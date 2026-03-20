async def get_cart(self, user_id: str) -> dict:
    cart_data = await cart_repository.get_cart(user_id)

    if not cart_data:
        raise ValueError("Carrito no encontrado o vacío")

    items = {
        product_id: int(quantity)
        for product_id, quantity in cart_data.items()
    }

    total_items = sum(items.values())

    return {
        "user_id": user_id,
        "items": items,
        "total_items": total_items
    }
