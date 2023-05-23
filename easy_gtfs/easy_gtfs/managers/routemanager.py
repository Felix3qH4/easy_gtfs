"""
    Module to manage multiple 'Route' models, write them to a file, load them from a file or parse them from a json object.

    Author: Felix Michelis
    Date: 23/05/2023
        dd/mm/yyyy
"""

from pydantic import ValidationError
from typing import Optional, List
import csv
from collections import Counter
import json


from ..utility import get_error_manager
from ..objects.route import Route
from ..models.errors import ErrorTypes, RouteError




class Routes():
    """A class to manage multiple 'Route' models and write them to a file, load them from a file or parse them from a json object."""

    def __init__(self, routes: List[Route] = None, file: str = None):
        """
            A class to manage multiple 'Route' models and write them to a file, load them from a file or parse them from a json object.

            :param routes [List[Route]] -- A list of 'Route' models, can be passed later with the respective function on function call
            :param file [str] -- The file to write to or load from, can be passed later with the respective function on function call
        """
        self.error_manager = get_error_manager()
        self.routes: List[Route] = routes
        self.file: str = file
    

    def to_file(self, routes: Optional[List[Route]] = None, file: Optional[str] = None) -> bool:
        """
            Writes a list of 'Route' models to a file in csv format.

            :param routes [Optional[List[Route]]] -- A list containing 'Route' models, if not given it will take 'self.routes' if set
            :param file [Optional[str]] -- The file to write to, if not given it will take 'self.file' if set

            :return bool -- True on success, else False or raises Error if not silent error enabled
        """

        if not routes:
            if self.routes == None:
                raise TypeError("Got no routes to write to file!")
            routes = self.routes

        if not file:
            if self.file == None:
                raise TypeError("Got no file to write to!")
            file = self.file


        headers: list = [variable for variable in routes[0].dict(exclude_unset=False).keys()]
        rows: list = []
        
        routes_ids = []
        
        for obj in routes:
            obj_as_dict = obj.dict(exclude_unset=False)
            routes_ids.append(obj_as_dict["route_id"])

            rows.append(obj_as_dict)

        if len(routes_ids) > 1:
            duplicates = [k for k, v in Counter(routes_ids).items() if v>1]
            if len(duplicates) > 0:
                if self.error_manager.is_silent_errors():
                    self.error_manager.add_error(RouteError(
                        caller = "RouteManager",
                        error_type=ErrorTypes.RouteErrorDuplicateID,
                        message="Multiple routes cannot have the same id!",
                        values = duplicates
                    ))
                    return False
                else:
                    raise ValueError(f"Multiple routes cannot have the same id! Got the following duplicate ids: {duplicates}")
                

        
                
        
            

        with open(file, "w", newline='') as _file:
            csvwriter = csv.DictWriter(_file, fieldnames=headers)
            csvwriter.writeheader()
            csvwriter.writerows(rows)


        return True



    def parse(self, routes_list: List[dict]) -> List[Route]:
        """
            Converts a list of dictionaries which each represent an 'Route' to a list of 'Route' models.
        """
        routes = []

        for route in routes_list:
            if self.is_valid_Route(route):
                routes.append(Route.parse_obj(route))
            else:
                if self.error_manager.is_silent_errors():
                    self.error_manager.add_error(RouteError(
                        caller = "RouteManager",
                        error_type = ErrorTypes.RouteErrorInvalidRoute,
                        message="Invalid Route from dict!",
                        values = [route]
                    ))
                    return False
                else:
                    raise ValueError(f"Invalid Route: {route}")

        return routes
    


    def load_file(self, file: Optional[str] = None) -> List[Route]:
        """
            Reads a file in csv format and outputs a list of 'Route' models contained in that file.

            :param file [Optional[str]] -- The file to read from, if not given it will take 'self.file' if its set

            :return List[Route] -- A list conatining 'Route' models
        """

        if not file:
            if self.file == None:
                raise TypeError("Got no file to load from!")
            file = self.file
        

        with open(file, "r") as _file:
            csvreader = list(csv.DictReader(_file)) # gives a list of dictionaries where each dict is a json representation of an Route

        routes = self.parse(csvreader)

        routes_ids = []

        for Route in routes:
            if Route.route_id in routes_ids:
                if self.error_manager.is_silent_errors():
                    self.error_manager.add_error(RouteError(
                        caller = "RouteManager",
                        error_type = ErrorTypes.RouteErrorDuplicateID,
                        message="Cannot have multiple routes with the same id!",
                        values = [Route.route_id]
                    ))
                    return False
                else:
                    raise ValueError("Cannot have multiple routes with the same id!")
                    
            routes_ids.append(Route.route_id)

        return routes

        
    def is_valid_Route(self, route: dict) -> bool:
        """
            Checks if a dict is a valid 'Route' model.

            :param Route [dict] -- The dict to validate
            
            :return bool -- 'True' if it contains a valid model, otherwise ('False', dict[argument_causing_error: error_message])
        """

        try:
            Route.parse_obj(route)

        except ValidationError as e:
            errors = {}

            for error in json.loads(e.json()):
                errors[error["loc"][0]] = error["msg"]

            return (False, errors)
        
        return True