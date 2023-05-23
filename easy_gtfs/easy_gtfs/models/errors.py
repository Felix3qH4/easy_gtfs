
from enum import Enum
from pydantic import BaseModel



class ErrorTypes(Enum):
    """
        GTFSError [0] -- General error with the GTFS feed
        GTFSErrorInvalidFile [1] -- The current file is of invalid format (many reasons, could not be csv format for example)
        GTFSErrorUnknownFile [2] -- The file should not be part of a GTFS Dataset
        GTFSErrorProcessReturnedFalse [3] -- One of the models (agency, route, ...) returned 'False' while parsing a file which caused the entire process to return False

        AgencyError [100] -- General error with the agency
        AgencyErrorDuplicateID [101] -- Two or more agencies have the same ID which is not allowed
        AgencyErrorInvalidAgency [102] -- The agency does not conform to the required format (usually when you try to parse a dict of a stop to a 'Agency' model)
        AgencyErrorTimezonesNotSame [103] -- If multiple agencies are present, all agencies must have the same timezone

        StopError [200] -- General error with the stop
        StopErrorDuplicateID [201] -- Two or more stops have the same ID which is not allowed
        StopErrorInvalidStop [202] -- The stop does not conform to the required format (usually when you try to parse a dict of a stop to a 'Stop' model)
        StopErrorMissingName [203] -- The name of the stop ('stop_name') is missing but required
        StopErrorMissingLatitude [204] -- The latitude of the stop ('stop_lat') is missing but required
        StopErrorMissingLongitude [205] -- The longitude of the stop ('stop_lon') is missing but required
        StopErrorMissingCoordinates [206] -- The coordinates ('stop_lat', 'stop_lon') are missing (at least one of them) but both are required
        StopErrorForbiddenParentStation [207] -- The stop has a parent station ('parent_station'), but due to its 'location_type' is not allowed to have one
        StopErrorMissingParentStation [208] -- The stop has no parent station ('parent_station'), but due to its 'location_type' it requires one

        RouteError [300] -- General error with the route
        RouteErrorDuplicateID [301] -- Two or more stops have the same ID which is not allowed
        RouteErrorInvalidStop [202] -- The route does not conform to the required format (usually when you try to parse a dict of a stop to a 'Route' model)
    """

    GTFSError: int = 0
    GTFSErrorInvalidFile: int = 1
    GTFSErrorUnknownFile: int = 2
    GTFSErrorProcessReturnedFalse: int = 3
    
    AgencyError: int = 100
    AgencyErrorDuplicateID: int = 101
    AgencyErrorInvalidAgency: int = 102
    AgencyErrorTimezonesNotSame: int = 103

    StopError: int = 200
    StopErrorDuplicateID: int = 201
    StopErrorInvalidStop: int = 202
    StopErrorMissingName: int = 203
    StopErrorMissingLatitude: int = 204
    StopErrorMissingLongitude: int = 205
    StopErrorMissingCoordinates: int = 206
    StopErrorForbiddenParentStation: int = 207
    StopErrorMissingParentStation: int = 208

    RouteError: int = 300
    RouteErrorDuplicateID: int = 301
    RouteErrorInvalidRoute: int = 302




class AgencyError(BaseModel):
    caller: str = "Agency"
    name: str = "AgencyError"
    error_type: ErrorTypes = ErrorTypes.AgencyError
    message: str
    values: list = []



class GTFSError(BaseModel):
    caller: str = "GTFS"
    name: str = "GTFSError"
    error_type: ErrorTypes = ErrorTypes.GTFSError
    message: str
    values: list = []



class StopError(BaseModel):
    caller: str = "Stop"
    name: str = "StopError"
    errory_type: ErrorTypes = ErrorTypes.StopError
    message: str
    values: list = []


class RouteError(BaseModel):
    caller: str = "Route"
    name: str = "RouteError"
    errory_type: ErrorTypes = ErrorTypes.RouteError
    message: str
    values: list = []