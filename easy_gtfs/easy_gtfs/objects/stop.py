from pydantic import BaseModel, validator
from typing import Optional, Union
from ..models.models import (
    LocationTypes,
    WheelchairBoarding_Parentless,
    WheelchairBoarding_Child,
    WheelchairBoarding_Entrance,
    WheelchairBoarding_Exit
)



class Stop(BaseModel):
    """
        https://developers.google.com/transit/gtfs/reference#stopstxt

        :param stop_id [str] -- Identifies a stop, station, or station entrance (station entrance refers to both entrances and exits) (multiple routes may use the same stop)
        :param stop_code [Optional[str]] -- Short text or a number that identifies the location for the riders
        :param stop_name [Optional[str]] -- Name of the stop that local people and tourists understand (required if location_type = 0, 1 or 2 )
        :param stop_desc [Optional[str]] -- Description of the location, that provides useful information
        :param stop_lat [Optional[float]] -- Latitude of the location (required if location_type = 0, 1 or 2)
        :param stop_lon [Optional[float]] -- Longitude of the location (required if location_type = 0, 1 or 2)
        :param zone_id [Optional[str]] -- The fare zone for the stop (required if providing fare information in 'fare_rules.txt' )
        :param stop_url [Optional[str]] -- URL of a web page about the location (should not be the same as the agency url and the route_url)
        :param location_type [Optional[LocationTypes]] -- The type of location (see 'models.models.LocationTypes' for details)
        :param parent_station [Optional[str]] -- ID of the parent location (required if location_type = 2, 3 or 4; optional if location_type = 0; forbidden if location_type = 1)
        :param stop_timezone [Optional[str]] -- The timezone of the location (if it has a parent station, it will inherit from the parent station)
        :param wheelchair_boarding [Optional[WheelchairBoarding]] -- Indicates if wheelchair boarding is possible from this stop (one of the following (models.models): [WheelchairBoardin_Parentless, WheelchairBoarding_Child, WheelchairBoarding_Entrance, WheelchairBoarding_Exit])
        :param level_id [Optional[str]] -- The level of the location (multiple stations can have the same level)
        :param platform_code [Optional[str]] -- Identifier for a platform stop (ex.: "A1" )
    """
    stop_id: str
    stop_code: Optional[str]
    stop_name: Optional[str]
    stop_desc: Optional[str]
    stop_lat: Optional[float]
    stop_lon: Optional[float]
    zone_id: Optional[str] # required if providing fare information using 'fare_rules.txt'
    stop_url: Optional[str]
    location_type: Optional[LocationTypes]
    parent_station: Optional[str]
    stop_timezone: Optional[str]
    wheelchair_boarding: Optional[Union[
        WheelchairBoarding_Parentless,
        WheelchairBoarding_Child,
        WheelchairBoarding_Entrance,
        WheelchairBoarding_Exit]
        ]
    level_id: Optional[str]
    platform_code: Optional[str]



    @validator("stop_name", always=True)
    def is_name_valid(cls, name, values):
        """
            The field 'stop_name' is required if the 'location_type' is one of the 'matching_types'
        """
        matching_types: list = [
            LocationTypes.STOP,
            LocationTypes.PLAFTORM,
            LocationTypes.STATION,
            LocationTypes.ENTRANCE,
            LocationTypes.EXIT
            ]
        
        if values["location_type"] != None:
            if values["location_type"] in matching_types:
                if name == None or len(name) < 1:
                    raise ValueError(f"is required if 'location_type' matches one of the following: \n {matching_types}")

        return name
    

    @validator("stop_lat", always=True)
    def is_lat_valid(cls, lat, values):
        """The field 'stop_lat' is required if the 'location_type' is one of the 'matching_types'"""
        matching_types: list = [
            LocationTypes.STOP,
            LocationTypes.PLAFTORM,
            LocationTypes.STATION,
            LocationTypes.ENTRANCE,
            LocationTypes.EXIT
        ]

        if values["location_type"] != None and values["location_type"] in matching_types:
            if lat == None:
                raise ValueError(f"is required if 'location_type' matches one of the following: \n {matching_types}")
            
        return lat
    

    @validator("stop_lon", always=True)
    def is_lat_valid(cls, lon, values):
        """The field 'stop_lon' is required if the 'location_type' is one of the 'matching_types'"""
        matching_types: list = [
            LocationTypes.STOP,
            LocationTypes.PLAFTORM,
            LocationTypes.STATION,
            LocationTypes.ENTRANCE,
            LocationTypes.EXIT
        ]

        if values["location_type"] != None and values["location_type"] in matching_types:
            if lon == None:
                raise ValueError(f"is required if 'location_type' matches one of the following: \n {matching_types}")
            
        return lon
    

    @validator("parent_station", always=True)
    def is_parent_station_valid(cls, parent_station, values):
        """
            Required:
                - Entrances/Exits (location_type=2)
                - Generic Nodes (location_type=3)
                - Boarding Areas (location_type=4)
            
            Forbidden:
                - Stations (location_type=1)

            Optional:
                - Stops/Platforms (location_type=0 or empty)
        """

        required: list = [
            LocationTypes.ENTRANCE,
            LocationTypes.EXIT,
            LocationTypes.GENERIC_NODE,
            LocationTypes.BOARDING_AREA
        ]

        forbidden: list = [
            LocationTypes.STATION
        ]

        if values["location_type"] != None:
            if values["location_type"] in required and parent_station == None or len(parent_station) < 1:
                raise ValueError(f"required if 'location_type' matches any of the following: \n {required}")
            
            elif values["location_type"] in forbidden and parent_station != None:
                raise ValueError(f"forbidden if 'location_type' matches any of the following: \n {forbidden}")
            
        return parent_station