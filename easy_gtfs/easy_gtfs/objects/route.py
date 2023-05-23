from pydantic import BaseModel, validator
from typing import Optional
from ..models.models import RouteType, ContinuousPickup, ContinuousDropOff



class Route(BaseModel):
    """
        https://developers.google.com/transit/gtfs/reference#routestxt

        :param route_id [str] -- The unique id for the route
        :param agency_id [Optional[str]] -- The agency using this route, only needed if multiple agencies are specified in 'agency.txt'
        :param route_short_name [Optional[str]] -- A short name for the route (required if 'route_long_name' is not set)
        :param route_long_name [Optional[str]] -- The long name for the route (required if 'route_short_name' is not set)
        
    """
    route_id: str
    agency_id: Optional[str]
    route_short_name: Optional[str]
    route_long_name: Optional[str]
    route_desc: Optional[str]
    route_type: RouteType
    route_url: Optional[str]
    route_color: Optional[str] = "FFFFFF"
    route_text_color: Optional[str] = "000000"
    route_sort_order: Optional[int]
    continuous_pickup: Optional[ContinuousPickup]
    continuous_drop_off: Optional[ContinuousDropOff]


    @validator("route_long_name", always=True)
    def is_route_long_name_valid(cls, route_long_name, values):
        """Either 'route_short_name' or 'route_long_name' is needed."""
        if values["route_short_name"] == None and route_long_name == None:
            raise ValueError("either 'route_short_name' or 'route_long_name' is needed")
        
        return route_long_name
    

    @validator("route_color", "route_text_color")
    def is_color_valid(cls, color):
        """Has to be a valid Hex color"""
        allowed_chars: str = "0123456789abcdefghijklmnopqrstuvwxyz"
        for char in color:
            if str(char).lower() not in allowed_chars:
                raise ValueError("has to be a valid hex color")
        
        return color
    
    
    @validator("route_sort_order")
    def is_route_sort_order_valid(cls, sort):
        if sort < 0:
            raise ValueError("has to be a non-negative integer")
        
        return sort
