
from enum import Enum
from pydantic import BaseModel



class ErrorTypes(Enum):
    """
        StopError [200] -- General error with the stop
        StopErrorDuplicateID [201] -- Two or more stops have the same ID which is not allowed
        StopErrorInvalidStop [202] -- The stop does not conform to the required format (usually when you try to parse a dict of a stop to a 'Stop' model)
        StopErrorMissingName [203] -- The name of the stop ('stop_name') is missing but required
        StopErrorMissingLatitude [204] -- The latitude of the stop ('stop_lat') is missing but required
        StopErrorMissingLongitude [205] -- The longitude of the stop ('stop_lon') is missing but required
        StopErrorMissingCoordinates [206] -- The coordinates ('stop_lat', 'stop_lon') are missing (at least one of them) but both are required
        StopErrorForbiddenParentStation [207] -- The stop has a parent station ('parent_station'), but due to its 'location_type' is not allowed to have one
        StopErrorMissingParentStation [208] -- The stop has no parent station ('parent_station'), but due to its 'location_type' it requires one
    """
    AgencyError: int = 0
    AgencyErrorDuplicateID: int = 1
    AgencyErrorInvalidAgency: int = 2
    AgencyErrorTimezonesNotSame: int = 3

    GTFSError: int = 100
    GTFSErrorInvalidFile: int = 101
    GTFSErrorUnknownFile: int = 102
    GTFSErrorProcessReturnedFalse: int = 103

    StopError: int = 200
    StopErrorDuplicateID: int = 201
    StopErrorInvalidStop: int = 202
    StopErrorMissingName: int = 203
    StopErrorMissingLatitude: int = 204
    StopErrorMissingLongitude: int = 205
    StopErrorMissingCoordinates: int = 206
    StopErrorForbiddenParentStation: int = 207
    StopErrorMissingParentStation: int = 208



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
