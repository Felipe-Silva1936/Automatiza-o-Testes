from dataclasses import dataclass
from typing import Optional


@dataclass
class Order:
    pet_id: int
    quantity: int
    id: Optional[int] = None
    ship_date: Optional[str] = None
    status: str = "placed"
    complete: bool = False

    def to_dict(self) -> dict:
        payload = {
            "petId": self.pet_id,
            "quantity": self.quantity,
            "status": self.status,
            "complete": self.complete,
        }
        if self.id is not None:
            payload["id"] = self.id
        if self.ship_date:
            payload["shipDate"] = self.ship_date
        return payload


class OrderBuilder:
    """Builder pattern for constructing Order payloads."""

    def __init__(self):
        self._id: Optional[int] = None
        self._pet_id: int = 1
        self._quantity: int = 1
        self._ship_date: Optional[str] = None
        self._status: str = "placed"
        self._complete: bool = False

    def with_id(self, order_id: int) -> "OrderBuilder":
        self._id = order_id
        return self

    def with_pet_id(self, pet_id: int) -> "OrderBuilder":
        self._pet_id = pet_id
        return self

    def with_quantity(self, quantity: int) -> "OrderBuilder":
        self._quantity = quantity
        return self

    def with_status(self, status: str) -> "OrderBuilder":
        self._status = status
        return self

    def with_ship_date(self, ship_date: str) -> "OrderBuilder":
        self._ship_date = ship_date
        return self

    def completed(self) -> "OrderBuilder":
        self._complete = True
        return self

    def build(self) -> Order:
        return Order(
            id=self._id,
            pet_id=self._pet_id,
            quantity=self._quantity,
            ship_date=self._ship_date,
            status=self._status,
            complete=self._complete,
        )
