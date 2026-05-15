from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.services.cart_service import CartService
from app.security import verify_api_key

router = APIRouter(
    prefix="/api/cart",
    tags=["cart"],
    dependencies=[Depends(verify_api_key)]
)
cart_service = CartService()


class AddItemRequest(BaseModel):
    product_id: str
    quantity: int


@router.post("/{user_id}/items", status_code=201)
async def add_item_to_cart(user_id: str, body: AddItemRequest):
    """
    Agrega o actualiza un producto en el carrito del usuario.

    Args:
        user_id: Identificador del usuario propietario del carrito.
        body: Cuerpo de la peticion con product_id y quantity.

    Returns:
        Diccionario con user_id, product_id y quantity guardados.
    """
    try:
        result = await cart_service.add_item(user_id, body.product_id, body.quantity)
        return result
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/{user_id}/ttl")
async def get_cart_ttl(user_id: str):
    """
    Retorna el tiempo de vida restante del carrito del usuario.

    Args:
        user_id: Identificador del usuario cuyo TTL se consultara.

    Returns:
        Diccionario con ttl_seconds, ttl_hours y warning.
    """
    try:
        result = await cart_service.get_ttl(user_id)
        return result
    except (ValueError, LookupError):
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/{user_id}/summary")
async def get_cart_summary(user_id: str):
    """
    Retorna un resumen estadistico del carrito del usuario.

    Args:
        user_id: Identificador del usuario cuyo resumen se consultara.

    Returns:
        Diccionario con distinct_products, total_units, top_product,
        ttl_seconds y expiring_soon.
    """
    try:
        result = await cart_service.get_summary(user_id)
        return result
    except (ValueError, LookupError):
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/{user_id}")
async def get_cart(user_id: str, page: int = 1, page_size: Optional[int] = None):
    """
    Retorna el contenido del carrito con soporte de paginacion opcional.

    Args:
        user_id: Identificador del usuario propietario del carrito.
        page: Numero de pagina (default 1).
        page_size: Cantidad de items por pagina. Si es None retorna todos.

    Returns:
        Diccionario con items, totales y datos de paginacion.
    """
    try:
        result = await cart_service.get_cart(user_id, page=page, page_size=page_size)
        return result
    except ValueError:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.delete("/{user_id}/items/{item_id}")
async def delete_item(user_id: str, item_id: str):
    """
    Elimina un producto especifico del carrito del usuario.

    Args:
        user_id: Identificador del usuario propietario del carrito.
        item_id: Identificador del producto a eliminar.

    Returns:
        Diccionario de confirmacion con user_id y product_id eliminado.
    """
    try:
        result = await cart_service.remove_item(user_id, item_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


class UpdateItemRequest(BaseModel):
    quantity: int


@router.put("/{user_id}/items/{item_id}")
async def update_item(user_id: str, item_id: str, body: UpdateItemRequest):
    """
    Actualiza la cantidad de un producto en el carrito del usuario.

    Args:
        user_id: Identificador del usuario propietario del carrito.
        item_id: Identificador del producto a actualizar.
        body: Cuerpo de la peticion con la nueva quantity.

    Returns:
        Diccionario con user_id, product_id y quantity actualizados.
    """
    try:
        result = await cart_service.update_item(user_id, item_id, body.quantity)
        return result
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.delete("/{user_id}")
async def clear_cart(user_id: str):
    """
    Elimina el carrito completo del usuario.

    Args:
        user_id: Identificador del usuario cuyo carrito se vaciara.

    Returns:
        Diccionario de confirmacion con user_id y mensaje.
    """
    try:
        result = await cart_service.clear_cart(user_id)
        return result
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
