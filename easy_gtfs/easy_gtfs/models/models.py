from enum import Enum
from pydantic import BaseModel


class LocationTypes(Enum):
    """
        Describes the type of location (station, stop, boarding area, ...)

        :STOP = 0
        :PLATFORM = 0
        :STATION = 1
        :ENTRANCE = 2
        :EXIT = 2
        :GENERIC_NODE = 3
        :BOARDING_AREA = 4
    """
    STOP: int = 0
    PLAFTORM: int = 0
    STATION: int = 1
    ENTRANCE: int = 2
    EXIT: int = 2
    GENERIC_NODE: int = 3
    BOARDING_AREA: int = 4


class WheelchairBoarding_Parentless(Enum):
    """
        Wheelchair accessibility for stops without parents

        :EMPTY = 0 -- No accessibility information for the stop
        :UNKNOWN = 0 -- equal to 'EMPTY'
        :PARTIALLY = 1 -- Some vehicles at this stop can be boarded by a rider in a wheelchair
        :NO = 2 -- Some vehicles at this stop can be boarded by a rider in a wheelchair
        :IMPOSSIBLE = 2 -- equal to 'NO'
    """
    EMPTY: int = 0
    UNKNOWN: int = 0
    PARTIALLY: int = 1
    NO: int = 2
    IMPOSSIBLE: int = 2


class WheelchairBoarding_Child(Enum):
    """
        Wheelchair accessibility for stops that are children of a parent stop

        :EMPTY = 0 -- Stop will inherit its wheelchair_boarding behavior from the parent station, if specified in the parent
        :UNKNOWN = 0 -- equal to 'EMPTY'
        :YES = 1 -- There exists some accessible path from outside the station to the specific stop/platform
        :POSSIBLE = 1 -- equal to 'YES'
        :NO = 2 -- There exists no accessible path from outside the station to the specific stop/platform
        :IMPOSSIBLE = 2 -- equal to 'NO'
    """
    EMPTY: int = 0 # will inherit accessibility from parent
    UNKNOWN: int = 0 # will inherit accessibility from parent
    YES: int = 1
    POSSIBLE: int = 1
    NO: int = 2
    IMPOSSIBLE: int = 2


class WheelchairBoarding_Entrance(Enum):
    """
        Wheelchair accessibility for entrances

        :EMPTY = 0 -- Station entrance will inherit its wheelchair_boarding behavior from the parent station, if specified for the parent
        :UNKOWN = 0 -- equal to 'EMPTY'
        :YES = 1 -- Station entrance is wheelchair accessible
        :POSSIBLE = 1 -- equal to 'YES'
        :NO = 2 -- No accessible path from station entrance to stops/platforms
        :IMPOSSIBLE = 2 -- equal to 'NO'

    """
    EMPTY: int = 0 # will inherit accessibility from parent
    UNKOWN: int = 0 # will inherit accessibility from parent
    YES: int = 1
    POSSIBLE: int = 1
    NO: int = 2
    IMPOSSIBLE: int = 2


class WheelchairBoarding_Exit(Enum):
    """
        Wheelchair accessibility for exits (equal to entrances)

        :EMPTY = 0 -- Station exit will inherit its wheelchair_boarding behavior from the parent station, if specified for the parent
        :UNKOWN = 0 -- equal to 'EMPTY'
        :YES = 1 -- Station exit is wheelchair accessible
        :POSSIBLE = 1 -- equal to 'YES'
        :NO = 2 -- No accessible path from station stops/platforms to exit
        :IMPOSSIBLE = 2 -- equal to 'NO'

    """
    EMPTY: int = 0 # will inherit accessibility from parent
    UNKOWN: int = 0 # will inherit accessibility from parent
    YES: int = 1
    POSSIBLE: int = 1
    NO: int = 2
    IMPOSSIBLE: int = 2



class RouteType(Enum):
    TRAM: int = 0
    Streetcar: int = 0
    LIGHT_RAIL: int = 0
    STREET_LEVEL_SYSTEM: int = 0

    SUBWAY: int = 1
    METRO: int = 1
    UNDERGROUND_LEVEL_SYSTEM: int = 1

    RAIL: int = 2
    INTERCITY: int = 2
    LONG_DISTANCE: int = 2

    BUS: int = 3
    LONG_DISTANCE_BUS: int = 3
    SHORT_DISTANCE_BUS: int = 3

    FERRY: int = 4
    LONG_DISTANCE_FERRY: int = 4
    SHORT_DISTANCE_FERRY: int = 4

    CABLE_TRAM: int = 5

    AERIAL_LIFT: int = 6
    SUSPENDED_CABLE_CAR: int = 6
    CABLE_CAR: int = 6
    GONDOLA_LIFT: int = 6
    AERIAL_TRAMWAY: int = 6
    CABLE_TRANSPORT: int = 6

    FUNICULAR: int = 7

    TROLLEYBUS: int = 11
    
    MONORAIL: int = 12




class ContinuousPickup(Enum):
    """
        Indicates whether a rider can board the transit vehicle anywhere along the vehicle’s travel path. The path is described by shapes.txt on every trip of the route.

            :CONTINUOUS = 0 -- Continuous stopping pickup
            :NO = 1 or empty -- No continuous stopping pickup
            :NON_CONTINUOUS = 1 -- equal to 'NO'
            :PHONE = 2 -- Must phone an agency to arrange continuous stopping pickup
            :PHONE_AGENCY = 2 -- equal to 'PHONE'
            :DRIVER = 3 -- Must coordinate with a driver to arrange continuous stopping pickup
            :COORDINATE_WITH_DRIVER = 3 -- equal to 'DRIVER'
    """
    CONTINUOUS: int = 0
    NO: int = 1
    NON_CONTINUOUS: int = 1
    PHONE: int = 2
    PHONE_AGENCY: int = 2
    DRIVER: int = 3
    COORDINATE_WITH_DRIVER: int = 3


class ContinuousDropOff(Enum):
    """
        Indicates whether a rider can alight from the transit vehicle at any point along the vehicle’s travel path. The path is described by shapes.txt on every trip of the route.

            :CONTINUOUS = 0 -- Continuous stopping drop-off
            :NO = 1 or empty -- No continuous stopping drop-off
            :NON_CONTINUOUS = 1 -- equal to 'NO'
            :PHONE = 2 -- Must phone an agency to arrange continuous stopping drop-off
            :PHONE_AGENCY = 2 -- equal to 'PHONE'
            :DRIVER = 3 -- Must coordinate with a driver to arrange continuous stopping drop-off
            :COORDINATE_WITH_DRIVER = 3 -- equal to 'DRIVER'
    """
    CONTINUOUS: int = 0
    NO: int = 1
    NON_CONTINUOUS: int = 1
    PHONE: int = 2
    PHONE_AGENCY: int = 2
    DRIVER: int = 3
    COORDINATE_WITH_DRIVER: int = 3


class DirectionId(Enum):
    """
        Indicates the direction of travel for a trip.

        :OUTBOUND = 0 -- Travel in one direction (e.g. outbound travel)
        :INBOUND = 1 -- Travel in the opposite direction (e.g. inbound travel)
    """
    OUTBOUND: int = 0
    INBOUND: int = 1


class WheelchairAccessible(Enum):
    """
        Indicates wheelchair accessibility.

        :UNKNOWN = 0 -- No accessibility information for the trip
        :YES = 1 -- Vehicle being used on this particular trip can accommodate at least one rider in a wheelchair
        :NO = 2 -- No riders in wheelchairs can be accommodated on this trip
    """
    UNKNOWN: int = 0
    YES: int = 1
    NO: int = 2



class BikeAllowed(Enum):
    """
        Indicates whether bikes are allowed.

        :UNKNOWN = 0 -- No bike information for the trip
        :YES = 1 -- Vehicle being used on this particular trip can accommodate at least one bicycle
        :NO = 2 -- No bicycles are allowed on this trip
    """
    UNKNOWN: int = 0
    YES: int = 1
    NO: int = 2
