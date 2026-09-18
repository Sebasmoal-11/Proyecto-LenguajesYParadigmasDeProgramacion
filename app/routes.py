from fastapi import APIRouter
from datetime import datetime
from app.schemas import UsuarioSchema
from app.database import usuarios_collection, consultas_collection
from app.models import usuario_model, consulta_model
from app.prolog_engine import obtener_recomendaciones_prolog
from app.ai_service import generar_explicacion_ia

router = APIRouter()


@router.get("/")
def home():
    return {"message": "API de ViajesPorElMundo funcionando correctamente"}


@router.post("/usuarios")
def crear_usuario(usuario: UsuarioSchema):
    usuario_dict = usuario.model_dump()
    usuario_dict["fecha_creacion"] = datetime.utcnow()

    resultado = usuarios_collection.insert_one(usuario_dict)
    nuevo_usuario = usuarios_collection.find_one({"_id": resultado.inserted_id})

    return {
        "message": "Usuario registrado correctamente",
        "usuario": usuario_model(nuevo_usuario)
    }


@router.get("/usuarios")
def listar_usuarios():
    usuarios = []
    for usuario in usuarios_collection.find():
        usuarios.append(usuario_model(usuario))
    return usuarios


@router.post("/planificar")
def planificar_viaje(usuario: UsuarioSchema):
    usuario_dict = usuario.model_dump()

    resultado_prolog = obtener_recomendaciones_prolog(usuario_dict)
    recomendaciones = resultado_prolog["recomendaciones"]
    ruta_sugerida = resultado_prolog["ruta_sugerida"]

    if not recomendaciones:
        explicacion_ia = (
            "No se encontraron destinos que coincidan exactamente con las "
            "preferencias ingresadas. Intenta cambiar el presupuesto, el clima "
            "o el tipo de viaje."
        )
    else:
        explicacion_ia = generar_explicacion_ia(usuario_dict, recomendaciones)

    consulta = {
        "usuario_nombre": usuario_dict["nombre"],
        "recomendaciones": recomendaciones,
        "ruta_sugerida": ruta_sugerida,
        "explicacion_ia": explicacion_ia,
        "fecha_consulta": datetime.utcnow()
    }

    consulta_guardada = consultas_collection.insert_one(consulta)
    nueva_consulta = consultas_collection.find_one({"_id": consulta_guardada.inserted_id})

    return {
        "message": "Plan de viaje generado correctamente",
        "consulta": consulta_model(nueva_consulta)
    }


@router.get("/consultas")
def listar_consultas():
    consultas = []
    for consulta in consultas_collection.find():
        consultas.append(consulta_model(consulta))
    return consultas