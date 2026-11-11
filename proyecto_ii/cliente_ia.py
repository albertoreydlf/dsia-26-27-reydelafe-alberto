"""Cliente de IA: pide a un modelo de lenguaje que explique la prediccion (mock o NVIDIA)."""

import logging
import os
from dataclasses import dataclass

import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# lee el fichero .env y deja NVIDIA_API_KEY disponible para os.getenv
load_dotenv()

# usamos NVIDIA porque da un endpoint gratis con una cuenta de desarrollador(me la paso david)
URL_NVIDIA = "https://integrate.api.nvidia.com/v1/chat/completions"
MODELO_NVIDIA = "nvidia/nemotron-3.5-super-vl-120b-a12b"


@dataclass
class Explicacion:
    """La respuesta del cliente, siempre con la misma forma venga de donde venga."""

    proveedor: str
    modelo: str
    texto: str


class ErrorClienteIA(RuntimeError):
    """Error propio para saber que el fallo viene de este cliente."""


def construir_prompt(habitos, prediccion, confianza):
    """Escribe la pregunta que le mandamos al modelo de lenguaje."""
    lineas_habitos = "\n".join(f"- {nombre}: {valor}" for nombre, valor in habitos.items())
    return (
        "Eres un asistente que explica resultados sobre el sueno de forma sencilla.\n"
        f"Un modelo ha predicho para esta persona la categoria '{prediccion}' "
        f"con una confianza de {confianza:.2f} (va de 0 a 1).\n"
        "Sus habitos antes de dormir son:\n"
        f"{lineas_habitos}\n"
        "Explica en 3 frases cortas y en espanol que significa y da un consejo practico. "
        "Si la confianza es baja, dilo. No des diagnosticos medicos."
    )


def explicar_con_nvidia(prompt, modelo=MODELO_NVIDIA):
    """Manda el prompt a la API de NVIDIA y devuelve el texto de la respuesta."""
    clave = os.getenv("NVIDIA_API_KEY")
    if not clave:
        raise ErrorClienteIA("Falta NVIDIA_API_KEY en el fichero .env")

    cabeceras = {"Authorization": f"Bearer {clave}"}  # asi se identifica quien llama
    # el cuerpo es lo que le mandamos a la API, va en formato JSON
    cuerpo = {
        # que modelo queremos que conteste (su id en el catalogo de NVIDIA)
        "model": modelo,
        # la conversacion: un solo mensaje, escrito por el usuario, con nuestro prompt
        "messages": [{"role": "user", "content": prompt}],
        # tope de largo de la respuesta (un token es mas o menos un trozo de palabra)
        "max_tokens": 1024,
        # creatividad: cerca de 0 contesta casi siempre igual, cerca de 1 varia mas
        "temperature": 0.2,
        # este modelo puede "pensar" antes de contestar, para 3 frases no hace falta
        "chat_template_kwargs": {"enable_thinking": False},
    }
    try:
        respuesta = requests.post(URL_NVIDIA, headers=cabeceras, json=cuerpo, timeout=60)
        respuesta.raise_for_status()  # salta si la API contesta con un error
    except requests.RequestException as error:
        logger.error("Fallo la llamada a NVIDIA: %s", error)
        raise ErrorClienteIA(f"Fallo la llamada a NVIDIA: {error}") from error

    # la respuesta trae una lista "choices", el texto esta en la primera
    texto = respuesta.json()["choices"][0]["message"].get("content") or ""
    if not texto.strip():
        raise ErrorClienteIA("NVIDIA contesto, pero la respuesta vino vacia")
    return texto.strip()


def explicar_prediccion(habitos, prediccion, confianza, proveedor="mock", modelo=MODELO_NVIDIA):
    """Devuelve una Explicacion. Con mock no usa internet, con nvidia llama a la API."""
    prompt = construir_prompt(habitos, prediccion, confianza)

    if proveedor == "mock":
        # respuesta fija para los tests: no gasta cuota ni necesita clave
        texto = (
            f"[mock] Prediccion: {prediccion} (confianza {confianza:.2f}). "
            "Aqui iria la explicacion del modelo de lenguaje."
        )
        return Explicacion(proveedor="mock", modelo="ninguno", texto=texto)

    if proveedor == "nvidia":
        texto = explicar_con_nvidia(prompt, modelo)
        return Explicacion(proveedor="nvidia", modelo=modelo, texto=texto)

    # Hugging Face (desactivado pq no tengo creditos)
    # Era la primera opcion. El token funcionaba, pero la cuenta gratuita tiene 0 creditos
    # y la API contesta 402 (Payment Required), asi que no se puede usar sin pagar.
    # Lo dejo comentado por si algun dia tengo creditos o pasa algo y lo puedo cambiar, habria que descomentarlo,
    # instalar huggingface_hub y poner el HF_TOKEN del .env.
    #
    # if proveedor == "hf":
    #     from huggingface_hub import InferenceClient
    #     cliente = InferenceClient(api_key=os.getenv("HF_TOKEN"), provider="auto")
    #     resultado = cliente.chat_completion(
    #         messages=[{"role": "user", "content": prompt}],
    #         model="openai/gpt-oss-120b",
    #         max_tokens=200,
    #     )
    #     texto = resultado.choices[0].message.content or ""
    #     return Explicacion(proveedor="huggingface", modelo="openai/gpt-oss-120b", texto=texto)

    raise ErrorClienteIA(f"Proveedor no soportado: {proveedor}")
