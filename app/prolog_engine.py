from pyswip import Prolog
from pathlib import Path


def normalizar_lista(lista):
    """
    Convierte strings a formato Prolog:
    'Costa Rica' -> 'costa_rica'
    """
    resultado = []
    for item in lista:
        item_normalizado = item.strip().lower().replace(" ", "_")
        resultado.append(item_normalizado)
    return resultado


def construir_lista_prolog(lista):
    """
    Convierte lista Python a texto de lista Prolog.
    ['japon', 'francia'] -> [japon,francia]
    """
    if not lista:
        return "[]"
    return "[" + ",".join(lista) + "]"


def obtener_recomendaciones_prolog(usuario: dict) -> dict:
    prolog = Prolog()

    ruta_prolog = Path(__file__).resolve().parent.parent / "prolog" / "viajes.pl"
    prolog.consult(str(ruta_prolog))

    visitados = normalizar_lista(usuario.get("paises_visitados", []))
    gustos = normalizar_lista(usuario.get("gustos", []))
    presupuesto = usuario.get("presupuesto", "").strip().lower()
    clima = usuario.get("clima_preferido", "").strip().lower()
    tipo = usuario.get("tipo_viaje", "").strip().lower()

    visitados_prolog = construir_lista_prolog(visitados)
    gustos_prolog = construir_lista_prolog(gustos)

    consulta = (
        f"recomendacion_final(Pais, {visitados_prolog}, "
        f"{gustos_prolog}, {presupuesto}, {clima}, {tipo})"
    )

    resultados = list(prolog.query(consulta))

    recomendaciones = []
    for resultado in resultados:
        pais = resultado["Pais"]
        pais_formateado = str(pais).replace("_", " ").title()
        if pais_formateado not in recomendaciones:
            recomendaciones.append(pais_formateado)

    ruta_sugerida = recomendaciones[:3]

    return {
        "recomendaciones": recomendaciones[:3],
        "ruta_sugerida": ruta_sugerida
    }