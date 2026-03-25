from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.cart_service import CartService

router = APIRouter(prefix="/api/cart", tags=["cart"])
cart_service = CartService()

class AddItemRequest(BaseModel):
    product_id: str
    quantity: int

@router.post("/{user_id}/items", status_code=201)
async def add_item_to_cart(user_id: str, body: AddItemRequest):
    try:
        result = await cart_service.add_item(user_id, body.product_id, body.quantity)
        return result
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
