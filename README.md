# Setup

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

## Run the Fastapi server

```bash
fastapi run main.py
```

## Using curl from CMD to test delivery API service

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
