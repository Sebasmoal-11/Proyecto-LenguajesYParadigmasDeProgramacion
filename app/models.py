from datetime import datetime


def usuario_model(usuario) -> dict:
    return {
        "id": str(usuario.get("_id", "")),
        "nombre": usuario.get("nombre", ""),
        "paises_visitados": usuario.get("paises_visitados", []),
        "gustos": usuario.get("gustos", []),
        "presupuesto": usuario.get("presupuesto", ""),
        "clima_preferido": usuario.get("clima_preferido", ""),
        "tipo_viaje": usuario.get("tipo_viaje", ""),
        "fecha_creacion": usuario.get("fecha_creacion", datetime.utcnow())
    }


def consulta_model(consulta) -> dict:
    return {
        "id": str(consulta.get("_id", "")),
        "usuario_nombre": consulta.get("usuario_nombre", ""),
        "recomendaciones": consulta.get("recomendaciones", []),
        "ruta_sugerida": consulta.get("ruta_sugerida", []),
        "explicacion_ia": consulta.get("explicacion_ia", ""),
        "fecha_consulta": consulta.get("fecha_consulta", datetime.utcnow())
    }