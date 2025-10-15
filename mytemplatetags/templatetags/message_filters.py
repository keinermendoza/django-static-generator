import json
from django import template

register = template.Library()

@register.filter(name='to_json')
def to_json(messages):
    """
    Convierte una lista de objetos Message (django.contrib.messages)
    en una lista de diccionarios serializables en JSON.
    """
    if not messages:
        return []

    result = []
    for m in messages:
        try:
            result.append({
                "level": getattr(m, "tags", ""),
                "message": getattr(m, "message", str(m))
            })
        except Exception:
            # fallback en caso de error
            result.append({"level": "info", "message": str(m)})
    return result