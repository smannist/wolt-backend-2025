# Setting up

My solution for a chance to get an interview with the best Finnish company ever created.

## Create and run the virtual environment

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

## Install requirements

```bash
pip install -r requirements.txt
```

## Run the FastAPI server

```bash
fastapi run main.py
```

# FastAPI docs

One of great features of FastAPI is its automatic doc generation which can be viewed via Swagger UI. Once the server is running, you can access the UI by navigation to http://0.0.0.0:8000/docs from your browser. The doc includes detailed information about the /api/v1/delivery-order-price endpoint, such as all accepted query parameters and their ranges, and possible HTTP status codes. Instead of manually curling the endpoint (as seen in next example) it's also possible to test the endpoint through the docs.

## Using curl to test delivery-order-price endpoint

First make sure that the server is running. You can then use CMD and curl to test the functionality of the endpoint by using the parameters described in FastAPI's docs.

Example:

```bash
curl "http://localhost:8000/api/v1/delivery-order-price?venue_slug=home-assignment-venue-helsinki&cart_value=1000&user_lat=60.17094&user_lon=24.93087"
```

Returns:

```json
{
  "total_price": 1190,
  "small_order_surcharge": 0,
  "cart_value": 1000,
  "delivery": {
    "fee": 190,
    "distance": 177
  }
}
```

# Testing

Make sure you are in virtual environment (check "Create and run the virtual environment" section how to enter venv) and that you run the command(s) from the root.

## Running unit tests

```bash
pytest tests/unit
```

## Running integration tests

```bash
pytest tests/integration
```

## Or simply run both

```bash
pytest
```
