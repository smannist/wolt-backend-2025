from pydantic import BaseModel

class Delivery(BaseModel):
    fee: int
    distance: int

class TotalDeliveryPrice(BaseModel):
    total_price: int
    small_order_surcharge: int
    cart_value: int
    delivery: Delivery
