from math import radians, sin, cos, sqrt, atan2

def get_distance_range(distance: float, distance_ranges: list[dict]) -> dict:
    """
    Finds the appropriate distance range for the given distance.

    Parameters:
    - distance: The distance in meters.
    - distance_ranges: A list of distance range dictionaries with `min` and `max`.

    Returns:
    - The matching range dictionary.
    """
    for range_item in distance_ranges:
        min_distance = range_item["min"]
        max_distance = range_item["max"]

        if min_distance <= distance < max_distance:
            return range_item

    raise ValueError("Distance is greater than delivery range")

def calculate_distance(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float
) -> int:
    """
    Calculates the straight line distance between two points in meters.
    The general idea is from: https://stackoverflow.com/questions/365826/calculate-distance-between-2-gps-coordinates

    Parameters:
    - lat1, lon1: Latitude and longitude of the first point in degrees.
    - lat2, lon2: Latitude and longitude of the second point in degrees.

    Returns:
    - Distance in meters rounded to nearest integer.
    """
    earth_radius_km = 6371

    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)

    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = (sin(d_lat / 2) ** 2 + sin(d_lon / 2) ** 2 * cos(lat1) * cos(lat2))
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return round(earth_radius_km * c * 1000)

def calculate_delivery_fee(
    base_price: int, 
    distance: float, 
    distance_range: dict
) -> float:
    """
    Calculates the delivery fee using the given formula:
    base_price + a + (b * distance) / 10

    Parameters:
    - base_price: The base price for delivery.
    - distance: The distance in meters.
    - distance_range: The range dictionary.

    Returns:
    - The calculated delivery fee rounded to nearest integer.
    """
    return round(base_price + distance_range["a"] + (distance_range["b"] * distance) / 10)

def calculate_surcharge(order_minimum_no_surcharge: int, cart_value: int) -> int:
    """Calculates the surcharge

    Returns:
    - The calculated surcharge
    """
    return max(0, order_minimum_no_surcharge - cart_value)

def calculate_total_price(delivery_fee: int, cart_value: int, surcharge: int) -> int:
    """Calculates the total fee which is a sum of delivery fee, cart value and
       surchage (if applied)

    Returns:
    - Total delivery price
    """
    return delivery_fee + cart_value + surcharge
