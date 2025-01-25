from exceptions import OutOfRangeException, EmptyCartException
from geopy.distance import distance


def get_distance_range(distance: float, distance_ranges: list[dict]) -> dict:
    """Finds the appropriate distance range for the given distance.

    Parameters:
    - distance: The distance in meters.
    - distance_ranges: A list of distance range dictionaries

    Returns:
    - The matching distance range dictionary.
    """
    for range_item in distance_ranges:
        min_distance = range_item["min"]
        max_distance = range_item["max"]
        if min_distance <= distance < max_distance:
            return range_item
    raise OutOfRangeException(
        status_code=400,
        message="We are sorry, this location is currently outside our delivery range.")


def calculate_distance(
        lon1: float,
        lat1: float,
        lon2: float,
        lat2: float) -> int:
    """Calculates the delivery distance in meters using the geopy library which utilizes Haversine formula
       and rounds the result to the nearest integer.

    Parameters:
    - lon1, lat1: Longitude and latitude of the first point.
    - lon2, lat2: Longitude and latitude of the second point.

    Returns:
    - Distance in meters rounded to the nearest integer.
    """
    return round(distance((lat1, lon1), (lat2, lon2)).meters)


def calculate_delivery_fee(
    base_price: int,
    distance: float,
    distance_range: dict
) -> float:
    """Calculates the delivery fee using the given formula:
       base_price + a + (b * distance) / 10.

    Parameters:
    - base_price: The base price for delivery.
    - distance: The distance in meters.
    - distance_range: The distance range dictionary.

    Returns:
    - The calculated delivery fee rounded to the nearest integer.
    """
    return round(base_price +
                 distance_range["a"] +
                 (distance_range["b"] *
                  distance) /
                 10)


def calculate_surcharge(
        order_minimum_no_surcharge: int,
        cart_value: int) -> int:
    """Calculates the surcharge,
       this is the difference between order_minimum_no_surcharge and cart value.

    Parameters:
    - order_minimum_no_surcharge: The surcharge base value.
    - cart_value: The cart value.

    Returns:
    - The total applied surcharge
    """
    return max(0, order_minimum_no_surcharge - cart_value)


def calculate_total_price(
        delivery_fee: int,
        cart_value: int,
        surcharge: int) -> int:
    """Calculates the total fee which is a sum of delivery fee, cart value and
       surchage (if applied).

    Returns:
    - The total delivery price
    """
    if cart_value <= 0:
        raise EmptyCartException(status_code=400, message="The cart is empty!")
    return delivery_fee + cart_value + surcharge
