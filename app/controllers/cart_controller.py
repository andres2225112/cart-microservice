@router.get("/{user_id}")
async def get_cart(user_id: str):
    try:
        result = await cart_service.get_cart(user_id)
        return result
    except ValueError:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
