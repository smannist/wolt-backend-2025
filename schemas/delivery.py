from pydantic import BaseModel

class DeliveryTransitDetails(BaseModel):
    fee: int
    distance: int

class DeliveryOrderSummary(BaseModel):
    total_price: int
    small_order_surcharge: int
    cart_value: int
    delivery: DeliveryTransitDetails
