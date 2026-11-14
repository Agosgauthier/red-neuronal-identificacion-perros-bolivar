"""Errores del dominio: los lanzan los services y los traduce la vista."""


class ValidacionError(ValueError):
    """Los datos que cargó la persona están incompletos o son inválidos."""


class ErrorRegistro(RuntimeError):
    """No se pudo guardar un perro encontrado (falla técnica, no de validación)."""
