query_errors = [
    {
        "field": "query.venue_slug",
        "error_type": "missing",
        "message": "venue_slug is required."
    },
    {
        "field": "query.cart_value",
        "error_type": "missing",
        "message": "cart_value is required."
    },
    {
        "field": "query.user_lat",
        "error_type": "missing",
        "message": "user_lat is required."
    },
    {
        "field": "query.user_lon",
        "error_type": "missing",
        "message": "user_lon is required."
    },
]


def test_endpoint_returns_correct_error_with_all_missing_query_parameters(
        test_client):
    """Tests that the API returns status code 400 with an error indicating that all parameters are missing"""
    response = test_client.get("/api/v1/delivery-order-price")
    assert response.status_code == 422
    for query_error in query_errors:
        assert query_error in response.json()["errors"]


def test_endpoint_returns_correct_error_with_missing_query_user_lon_param(
        test_client):
    """Tests that the API returns status code 400 with an error indication that single parameter is missing"""
    response = test_client.get(
        "/api/v1/delivery-order-price?venue_slug=home-assignment-venue-helsinki&cart_value=1000&user_lat=60.17094")
    assert response.status_code == 422
    assert any(
        error["message"] == "user_lon is required."
        for error in response.json()["errors"]
    )


def test_endpoint_returns_correct_error_with_unacceptable_venue_param(
        test_client):
    """Tests that the API returns status code 400 with an error indicating that the given venue is unaccepted"""
    response = test_client.get(
        "/api/v1/delivery-order-price?venue_slug=home-assignment-venue-seoul&user_lat=60.17094&user_lon=24.93087")
    assert response.status_code == 422
    assert any(
        error["message"] == "home-assignment-venue-seoul is not a valid venue"
        for error in response.json()["errors"]
    )


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
    assert response.headers.get("X-Exception-Type") == "OutOfRangeException"
    assert response.json() == {
        "detail": "We are sorry, this location is currently outside our delivery range."
    }


def test_return_empty_cart_error(test_client):
    """Tests that the API returns 400 and an error message for empty cart"""
    response = test_client.get(
        "/api/v1/delivery-order-price?venue_slug=home-assignment-venue-helsinki&cart_value=0&user_lat=60.17094&user_lon=24.93087")
    assert response.status_code == 400
    assert response.headers.get("X-Exception-Type") == "EmptyCartException"
    assert response.json() == {"detail": "The cart is empty!"}
