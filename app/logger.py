import logging
import sys

def get_logger(name: str) -> logging.Logger:
    """
    Retorna un logger configurado para el microservicio.
    Uso: logger = get_logger(__name__) al inicio de cada módulo.
    El parámetro __name__ genera nombres como 'app.services.cart_service',
    lo que permite filtrar logs por capa en Railway o en cualquier agregador.
    """
    logger = logging.getLogger(name)
    # Evitar duplicar handlers si el logger ya fue configurado
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    # Formato: timestamp | nivel | nombre del módulo | mensaje
    formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.propagate = False  # evitar duplicación en el root logger
    return logger
