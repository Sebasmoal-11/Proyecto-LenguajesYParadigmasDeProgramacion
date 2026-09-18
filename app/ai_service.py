import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "gemma3"


def generar_prompt(usuario: dict, recomendaciones: list) -> str:
    nombre = usuario.get("nombre", "")
    gustos = ", ".join(usuario.get("gustos", []))
    visitados = ", ".join(usuario.get("paises_visitados", [])) or "ninguno"
    presupuesto = usuario.get("presupuesto", "")
    clima = usuario.get("clima_preferido", "")
    tipo_viaje = usuario.get("tipo_viaje", "")

    return f"""
Eres un asistente de planificación de viajes.
Redacta una explicación breve, clara y natural en español.

Datos del usuario:
- Nombre: {nombre}
- Gustos: {gustos}
- Países visitados: {visitados}
- Presupuesto: {presupuesto}
- Clima preferido: {clima}
- Tipo de viaje: {tipo_viaje}

Destinos recomendados por reglas lógicas:
- {", ".join(recomendaciones)}

Instrucciones:
- Explica por qué esos destinos coinciden con el perfil.
- Menciona que no repiten países ya visitados.
- Usa un tono formal pero sencillo.
- Hazlo en un solo párrafo.
""".strip()


def generar_explicacion_local_ollama(prompt: str) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=120)
    response.raise_for_status()

    data = response.json()
    return data.get("response", "").strip()


def generar_explicacion_respaldo(usuario: dict, recomendaciones: list) -> str:
    gustos = ", ".join(usuario.get("gustos", []))
    visitados = ", ".join(usuario.get("paises_visitados", [])) or "ninguno"

    return (
        f"Según el análisis realizado, se recomienda a {usuario.get('nombre')} "
        f"visitar {', '.join(recomendaciones)}. Estos destinos coinciden con sus "
        f"gustos ({gustos}), con su preferencia de clima "
        f"'{usuario.get('clima_preferido')}', su presupuesto "
        f"'{usuario.get('presupuesto')}' y su tipo de viaje "
        f"'{usuario.get('tipo_viaje')}'. Además, la recomendación evita países ya "
        f"visitados previamente ({visitados}), por lo que ofrece una experiencia "
        f"nueva y alineada con el perfil del viajero."
    )


def generar_explicacion_ia(usuario: dict, recomendaciones: list) -> str:
    try:
        prompt = generar_prompt(usuario, recomendaciones)
        explicacion = generar_explicacion_local_ollama(prompt)

        if explicacion:
            return explicacion

        return generar_explicacion_respaldo(usuario, recomendaciones)

    except Exception:
        return generar_explicacion_respaldo(usuario, recomendaciones)