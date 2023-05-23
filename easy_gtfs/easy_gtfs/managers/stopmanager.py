"""
    Module to manage multiple 'Stop' models, write them to a file, load them from a file or parse them from a json object.

    Author: Felix Michelis
    Date: 19/05/2023
        dd/mm/yyyy
"""
from pydantic import ValidationError
from typing import Optional, List
import csv
from collections import Counter
import json


from ..utility import get_error_manager
from ..objects.stop import Stop
from ..models.errors import ErrorTypes, StopError


"""
    TODO: 'level_id' has to be one from 'levels.level_id'
"""

class Stops():
    """A class to manage multiple 'Stop' models and write them to a file, load them from a file or parse them from a json object."""

    def __init__(self, stops: List[Stop] = None, file: str = None):
        """
            A class to manage multiple 'Stop' models and write them to a file, load them from a file or parse them from a json object.

            :param agencies [List[Stop]] -- A list of 'Stop' models, can be passed later with the respective function on function call
            :param file [str] -- The file to write to or load from, can be passed later with the respective function on function call
        """
        self.error_manager = get_error_manager()
        self.stops: List[Stop] = stops
        self.file: str = file
    

    def to_file(self, stops: Optional[List[Stop]] = None, file: Optional[str] = None) -> bool:
        """
            Writes a list of 'Stop' models to a file in csv format.

            :param stopss [Optional[List[Stop]]] -- A list containing 'Stop' models, if not given it will take 'self.stops' if set
            :param file [Optional[str]] -- The file to write to, if not given it will take 'self.file' if set

            :return bool -- True on success, else False or raises Error if not silent error enabled
        """

        if not agencies:
            if self.stops == None:
                raise TypeError("Got no stops to write to file!")
            agencies = self.stops

        if not file:
            if self.file == None:
                raise TypeError("Got no file to write to!")
            file = self.file


        headers: list = [variable for variable in stops[0].dict(exclude_unset=False).keys()] # create a list of the headers for the csv file
        rows: list = []
        
        stops_ids = [] # this list stores the ids of all the stops that will be written to the file so we can verify that no agencies have the same id
        for obj in stops:
            obj_as_dict = obj.dict(exclude_unset=False)
            obj_as_dict["wheelchair_boarding"] = obj_as_dict["wheelchair_boarding"].value
            obj_as_dict["location_type"] = obj_as_dict["location_type"].value
            
            stops_ids.append(obj_as_dict["stop_id"]) # add the id of the stop to our ids list for verification later on

            
            if obj_as_dict["location_type"] in [0, 1, 2]:
                ## Stop Name
                if len(obj_as_dict["stop_name"]) < 1:
                    if self.error_manager.is_silent_errors():
                        self.error_manager.add_error(StopError(
                            error_type=ErrorTypes.StopErrorMissingName,
                            message="If 'location_type' is 0, 1 or 2, the 'stop_name' has to be provided!",
                            values=[obj_as_dict]
                        ))
                    else:
                        raise ValueError(f"If 'location_type' is 0, 1 or 2, the 'stop_name' has to be provided! \n {obj_as_dict}")
                
                ## Stop Lat + Lon
                elif len(obj_as_dict["stop_lat"]) < 1 or len(obj_as_dict["stop_lon"]) < 1:
                    if self.error_manager.is_silent_errors():
                        self.error_manager.add_error(StopError(
                            error_type=ErrorTypes.StopErrorMissingCoordinates,
                            message="If 'location_type' is 0, 1 or 2, the 'stop_lat' and 'stop_lon' have to be provided!",
                            values=[obj_as_dict]
                        ))
                    else:
                        raise ValueError(f"If 'location_type' is 0, 1 or 2, the 'stop_lat' and 'stop_lon' have to be provided! \n {obj_as_dict}")
                    

            ## Parent Station
            if obj_as_dict["location_type"] == 1:
                if len(obj_as_dict["parent_station"]) > 0:
                    if self.error_manager.is_silent_errors():
                        self.error_manager.add_error(StopError(
                            error_type=ErrorTypes.StopErrorForbiddenParentStation,
                            message="If 'location_type' is 1, passing a parent station ('parent_station') is forbidden!",
                            values=[obj_as_dict]
                        ))
                    else:
                        raise ValueError(f"If 'location_type' is 1, passing a parent station ('parent_station') is forbidden! \n {obj_as_dict}")
                    
            if obj_as_dict["location_type"] in [2, 3, 4]:
                if len(obj_as_dict["parent_station"]) < 1:
                    if self.error_manager.is_silent_errors():
                        self.error_manager.add_error(StopError(
                            error_type=ErrorTypes.StopErrorMissingParentStation,
                            message="If 'location_type' is 2, 3 or 4, passing a parent station ('parent_station') is required!",
                            values=[obj_as_dict]
                        ))
                    else:
                        raise ValueError(f"If 'location_type' is 2, 3 or 4, passing a parent station ('parent_station') is required! \n {obj_as_dict}")
                    

            rows.append(obj_as_dict) # add the Stop as json to our rows that will be written to the csv file





        if len(stops_ids) > 1:
            duplicates = [k for k, v in Counter(stops_ids).items() if v>1] # returns a list with all duplicate ids; if the id '123' was for example at least 2 times in the ids list the output would be: ['123']
            if len(duplicates) > 0:
                if self.error_manager.is_silent_errors():
                    self.error_manager.add_error(StopError(
                        error_type=ErrorTypes.StopErrorDuplicateID,
                        message="Multiple stops cannot have the same id!",
                        values = duplicates
                    ))
                    return False
                else:
                    raise ValueError(f"Multiple stops cannot have the same id! Got the following duplicate ids: {duplicates}")
            



        with open(file, "w", newline='') as _file:
            csvwriter = csv.DictWriter(_file, fieldnames=headers)
            csvwriter.writeheader()
            csvwriter.writerows(rows)


        return True





    def parse(self, stops_list: List[dict]) -> List[Stop]:
        """
            Converts a list of dictionaries which each represent an 'Stop' to a list of 'Stop' models.
        """
        stops = []

        for Stop in stops_list:
            if self.is_valid_Stop(Stop):
                stops.append(Stop.parse_obj(Stop))
            else:
                if self.error_manager.is_silent_errors():
                    self.error_manager.add_error(StopError(
                        error_type = ErrorTypes.StopErrorInvalidStop,
                        message="Invalid stop from dict!",
                        values = [Stop]
                    ))
                    return False
                else:
                    raise ValueError(f"Invalid stop: {Stop}")

        return stops
    


    def load_file(self, file: Optional[str] = None) -> List[Stop]:
        """
            Reads a file in csv format and outputs a list of 'Stop' models contained in that file.

            :param file [Optional[str]] -- The file to read from, if not given it will take 'self.file' if its set

            :return List[Stop] -- A list conatining 'Stop' models
        """

        if not file:
            if self.file == None:
                raise TypeError("Got no file to load from!")
            file = self.file
        

        with open(file, "r") as _file:
            csvreader = list(csv.DictReader(_file)) # gives a list of dictionaries where each dict is a json representation of an Stop

        stops = self.parse(csvreader)

        stops_ids = []

        for Stop in stops:
            ## Stop ID
            if Stop.stop_id in stops_ids:
                if self.error_manager.is_silent_errors():
                    self.error_manager.add_error(StopError(
                        error_type = ErrorTypes.StopErrorDuplicateID,
                        message="Cannot have multiple stops with the same id!",
                        values = [Stop.stop_id]
                    ))
                    return False
                else:
                    raise ValueError("Cannot have multiple stops with the same id!")
                
            
            if Stop.location_type in [0, 1, 2]:
                ## Stop Name
                if len(Stop.stop_name) < 1:
                    if self.error_manager.is_silent_errors():
                        self.error_manager.add_error(StopError(
                            error_type=ErrorTypes.StopErrorMissingName,
                            message="If 'location_type' is 0, 1 or 2, the 'stop_name' has to be provided!",
                            values=[Stop]
                        ))
                    else:
                        raise ValueError(f"If 'location_type' is 0, 1 or 2, the 'stop_name' has to be provided! \n {Stop}")
                
                ## Stop Lat + Lon
                elif len(Stop.stop_lat) < 1 or len(Stop.stop_lon) < 1:
                    if self.error_manager.is_silent_errors():
                        self.error_manager.add_error(StopError(
                            error_type=ErrorTypes.StopErrorMissingCoordinates,
                            message="If 'location_type' is 0, 1 or 2, the 'stop_lat' and 'stop_lon' have to be provided!",
                            values=[Stop]
                        ))
                    else:
                        raise ValueError(f"If 'location_type' is 0, 1 or 2, the 'stop_lat' and 'stop_lon' have to be provided! \n {Stop}")
                    

            ## Parent Station
            if Stop.location_type == 1:
                if len(Stop.parent_station) > 0:
                    if self.error_manager.is_silent_errors():
                        self.error_manager.add_error(StopError(
                            error_type=ErrorTypes.StopErrorForbiddenParentStation,
                            message="If 'location_type' is 1, passing a parent station ('parent_station') is forbidden!",
                            values=[Stop]
                        ))
                    else:
                        raise ValueError(f"If 'location_type' is 1, passing a parent station ('parent_station') is forbidden! \n {Stop}")
                    
            if Stop.location_type in [2, 3, 4]:
                if len(Stop.parent_station) < 1:
                    if self.error_manager.is_silent_errors():
                        self.error_manager.add_error(StopError(
                            error_type=ErrorTypes.StopErrorMissingParentStation,
                            message="If 'location_type' is 2, 3 or 4, passing a parent station ('parent_station') is required!",
                            values=[Stop]
                        ))
                    else:
                        raise ValueError(f"If 'location_type' is 2, 3 or 4, passing a parent station ('parent_station') is required! \n {Stop}")
                    


            stops_ids.append(Stop.stop_id)

        return stops

        


    def is_valid_Stop(self, stop: dict) -> bool:
        """
            Checks if a dict is a valid 'Stop' model.

            :param stop [dict] -- The dict to validate
            
            :return bool -- 'True' if it contains a valid model, otherwise ('False', dict[argument_causing_error: error_message])
        """

        try:
            Stop.parse_obj(Stop)

        except ValidationError as e:
            errors = {}

            for error in json.loads(e.json()):
                errors[error["loc"][0]] = error["msg"]

            return (False, errors)
        
        return True