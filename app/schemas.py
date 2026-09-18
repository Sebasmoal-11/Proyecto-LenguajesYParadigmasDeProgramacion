from pydantic import BaseModel
from typing import List


class UsuarioSchema(BaseModel):
    nombre: str
    paises_visitados: List[str]
    gustos: List[str]
    presupuesto: str
    clima_preferido: str
    tipo_viaje: str


class ConsultaResponseSchema(BaseModel):
    usuario_nombre: str
    recomendaciones: List[str]
    ruta_sugerida: List[str]
    explicacion_ia: str