
def test_endpoint_returns_correct_error_with_all_missing_query_parameters(
        test_client):
    """Tests that the API returns status code 400 with an error indicating that all parameters are missing"""
    response = test_client.get("/api/v1/delivery-order-price")
    assert response.status_code == 422
    assert response.json() == {
        "detail": "Missing query parameters: venue_slug, venue_slug, cart_value, user_lat, user_lon"
    }


def test_endpoint_returns_correct_error_with_missing_query_user_lon_param(
        test_client):
    """Tests that the API returns status code 400 with an error indication that single parameter is missing"""
    response = test_client.get(
        "/api/v1/delivery-order-price?venue_slug=home-assignment-venue-helsinki&cart_value=1000&user_lat=60.17094")
    assert response.status_code == 422
    assert response.json() == {
        "detail": "Missing query parameters: user_lon"
    }


def test_endpoint_returns_correct_error_with_unacceptable_venue_param(
        test_client):
    """Tests that the API returns status code 400 with an error indicating that the given venue is unaccepted"""
    response = test_client.get(
        "/api/v1/delivery-order-price?venue_slug=home-assignment-venue-seoul&cart_value=1000&user_lat=60.17094&user_lon=24.93087")
    assert response.status_code == 422
    assert response.json() == {
        "detail": "Invalid venue: home-assignment-venue-seoul"
    }


def test_delivery_fee_is_returned_when_valid_query_parameters_are_present(
        test_client):
    """Tests that the API returns 200 and the delivery fee is calculated correctly with valid parameters"""
    response = test_client.get(
        "/api/v1/delivery-order-price?venue_slug=home-assignment-venue-helsinki&cart_value=1000&user_lat=60.17094&user_lon=24.93087")
    assert response.status_code == 200
    assert response.json() == {
        "total_price": 1190,
        "small_order_surcharge": 0,
        "cart_value": 1000,
        "delivery": {
            "fee": 190,
            "distance": 177
        }
    }


def test_return_out_of_range_delivery_error(test_client):
    """Tests that the API returns 400 and an error message for out of range delivery"""
    response = test_client.get(
        "/api/v1/delivery-order-price?venue_slug=home-assignment-venue-helsinki&cart_value=1000&user_lat=60.17094&user_lon=21.93087")
    assert response.status_code == 400
    assert response.json() == {
        "detail": "We are sorry, this location is currently outside our delivery range."
    }


def test_return_empty_cart_error(test_client):
    """Tests that the API returns 400 and an error message for empty cart"""
    response = test_client.get(
        "/api/v1/delivery-order-price?venue_slug=home-assignment-venue-helsinki&cart_value=0&user_lat=60.17094&user_lon=24.93087")
    assert response.status_code == 400
    assert response.json() == {"detail": "The cart is empty!"}
