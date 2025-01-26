from exceptions import OutOfRangeException, EmptyCartException
from tests.delivery_constants import DISTANCE_RANGES
from services.delivery import (
    get_distance_range,
    calculate_delivery_fee,
    calculate_distance,
    calculate_surcharge,
    calculate_total_price
)


def test_distance_range_is_selected_correctly_with_inclusive_min_range():
    """Tests that the selected distance falls on the correct range when the distance is exactly within inclusive minimum range."""
    assert get_distance_range(0, DISTANCE_RANGES) == DISTANCE_RANGES[0]
    assert get_distance_range(1000, DISTANCE_RANGES) == DISTANCE_RANGES[2]
    assert get_distance_range(1500, DISTANCE_RANGES) == DISTANCE_RANGES[3]


def test_distance_range_is_selected_correctly_with_exclusive_max_range():
    """Tests that the selected distance falls on the correct range when the distance is slightly below the maximum range."""
    assert get_distance_range(499, DISTANCE_RANGES) == DISTANCE_RANGES[0]
    assert get_distance_range(999, DISTANCE_RANGES) == DISTANCE_RANGES[1]
    assert get_distance_range(1499, DISTANCE_RANGES) == DISTANCE_RANGES[2]


def test_delivery_fee_is_calculated_correctly():
    """Tests that the delivery free is calculated correctly with given parameters.

    - Formula: base_price + a + (b * distance) / 10
    - Expected: 199 + 100 + 0 * 600 / 10 = 299
    """
    base_price = 199
    distance = 600
    assert calculate_delivery_fee(
        base_price, distance, DISTANCE_RANGES[1]) == 299


def test_distance_is_calculated_correctly():
    """Tests that the straight line distance between two points is calculated correctly."""
    user_lon, user_lat = 24.93087, 60.17094
    venue_lon, venue_lat = 24.92813512, 60.17012143
    distance = calculate_distance(user_lon, user_lat, venue_lon, venue_lat)
    assert distance == 177  # meters


def test_surcharge_is_calculated_correctly_with_positive_difference():
    """Tests that the minimum surcharge is calculated correctly when the difference is positive.

    min_surchage - cart value = 1000 - 300 = 700
    """
    assert calculate_surcharge(1000, 300) == 700


def test_surcharge_is_zero_with_negative_diffence():
    """Tests that the minimum surcharge is calculated correctly when the difference is negative.

    min_surchage - cart value = 1000 - 1500 = -500
    negative value should result in no applied surcharge
    """
    assert calculate_surcharge(1000, 1500) == 0


def test_total_price_is_calculated_correctly_with_valid_values():
    """Tests that the total price is summed correctly.

    300 + 1500 + 800 = 2600
    """
    delivery_fee = 300
    cart_value = 1500
    surcharge = 800
    assert calculate_total_price(delivery_fee, cart_value, surcharge) == 2600


def test_empty_cart_raises_correct_exception():
    """Tests that the correct exception is raised when the cart is empty."""
    delivery_fee = 300
    cart_value = 0
    surcharge = 800
    try:
        calculate_total_price(delivery_fee, cart_value, surcharge) == 2600
    except EmptyCartException as e:
        assert e.detail == "The cart is empty!"
    else:
        assert False, "Expected EmptyCartException for empty cart."


def test_greatly_out_of_delivery_range_raises_correct_exception():
    """Tests that the correct exception is raised when the distance is greater than delivery range with large distance difference."""
    try:
        get_distance_range(20000, DISTANCE_RANGES)
    except OutOfRangeException as e:
        assert e.detail == "We are sorry, this location is currently outside our delivery range."
    else:
        assert False, "Expected OutOfRangeException for out-of-range distance."


def test_exactly_out_of_delivery_range_raises_correct_exception():
    """Tests that the correct exception is raised when the distance is exactly within unaccepted delivery range."""
    try:
        get_distance_range(10000, DISTANCE_RANGES)
    except OutOfRangeException as e:
        assert e.detail == "We are sorry, this location is currently outside our delivery range."
    else:
        assert False, "Expected OutOfRangeException for out-of-range distance."
