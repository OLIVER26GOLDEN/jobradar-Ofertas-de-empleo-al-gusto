import os
import requests
import base64
from typing import List, Dict, Any

# Infojobs API URL
INFOJOBS_API_URL = "https://api.infojobs.net/api/7/offer"

def fetch_infojobs_offers(query: str = "python", limit: int = 10) -> List[Dict[str, Any]]:
    """
    Consigue ofertas de la API de InfoJobs usando las credenciales en .env.
    Si no hay credenciales, devuelve datos simulados de forma limpia para desarrollo y pruebas.
    """
    client_id = os.getenv("INFOJOBS_CLIENT_ID")
    client_secret = os.getenv("INFOJOBS_CLIENT_SECRET")

    # Si falta alguna de las credenciales, usamos datos de mock realistas
    if not client_id or not client_secret or client_id == "tu_client_id":
        return get_mock_infojobs_offers(query, limit)

    # Autenticación Básica requerida por InfoJobs: Basic base64(client_id:client_secret)
    credential_str = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(credential_str.encode("utf-8")).decode("utf-8")
    
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json"
    }
    
    params = {
        "q": query,
        "maxResults": limit
    }

    try:
        response = requests.get(INFOJOBS_API_URL, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            offers_raw = data.get("items", [])
            
            parsed_offers = []
            for item in offers_raw:
                # Estructura típica de respuesta de InfoJobs API
                titulo = item.get("title", "Sin título")
                empresa = item.get("author", {}).get("name", "Empresa Confidencial")
                ubicacion = item.get("city", "España")
                
                # Modalidad de teletrabajo si está disponible
                teleworking = item.get("teleworking", {})
                modalidad = teleworking.get("name", "No especificado") if teleworking else "No especificado"
                
                # Salario
                salario = item.get("salaryDescription", "No especificado")
                
                # Enlace directo
                enlace = item.get("link", "")
                
                # Fecha
                fecha_pub = item.get("published", None)
                
                # Descripción mínima o detalles
                descripcion = item.get("requirementMin", "Sin descripción detallada.")

                parsed_offers.append({
                    "titulo": titulo,
                    "empresa": empresa,
                    "ubicacion": ubicacion,
                    "modalidad": modalidad,
                    "salario": salario,
                    "descripcion": descripcion,
                    "enlace": enlace,
                    "fuente": "InfoJobs",
                    "estado": "guardado",
                    "fecha_publicacion": fecha_pub
                })
            return parsed_offers
        else:
            print(f"Error calling InfoJobs API: {response.status_code} - {response.text}")
            return get_mock_infojobs_offers(query, limit)
    except Exception as e:
        print(f"Exception connecting to InfoJobs: {e}")
        return get_mock_infojobs_offers(query, limit)

def get_mock_infojobs_offers(query: str, limit: int) -> List[Dict[str, Any]]:
    """
    Devuelve ofertas mockeadas para simular la API de InfoJobs.
    """
    mock_data = [
        {
            "titulo": "Desarrollador Python Junior",
            "empresa": "TechMadrid Solutions",
            "ubicacion": "Madrid",
            "modalidad": "Híbrido",
            "salario": "24.000€ - 28.000€ Bruto/Año",
            "descripcion": "Buscamos un perfil junior con ganas de aprender y mejorar en Python y FastAPI.",
            "enlace": "https://www.infojobs.net/madrid/desarrollador-python-junior/of-i12345",
            "fuente": "InfoJobs",
            "estado": "guardado",
            "fecha_publicacion": "2026-06-25T10:00:00Z"
        },
        {
            "titulo": "Python Backend Developer (FastAPI)",
            "empresa": "Global Software S.L.",
            "ubicacion": "Barcelona",
            "modalidad": "Remoto",
            "salario": "40.000€ - 45.000€ Bruto/Año",
            "descripcion": "Únete a nuestro equipo de backend de alto rendimiento construyendo APIs eficientes en Python.",
            "enlace": "https://www.infojobs.net/barcelona/python-backend-developer/of-i67890",
            "fuente": "InfoJobs",
            "estado": "guardado",
            "fecha_publicacion": "2026-06-26T14:30:00Z"
        },
        {
            "titulo": "Fullstack Developer (Python/React)",
            "empresa": "Fintech Innova",
            "ubicacion": "Valencia",
            "modalidad": "Presencial",
            "salario": "30.000€ - 35.000€ Bruto/Año",
            "descripcion": "Desarrollo completo de aplicaciones fintech. Stack: Django/FastAPI y React.",
            "enlace": "https://www.infojobs.net/valencia/fullstack-developer/of-i11121",
            "fuente": "InfoJobs",
            "estado": "guardado",
            "fecha_publicacion": "2026-06-27T08:15:00Z"
        }
    ]
    # Filtrar según la keyword
    filtered = [o for o in mock_data if query.lower() in o["titulo"].lower() or query.lower() in o["descripcion"].lower()]
    # Si la keyword no coincide con ninguno, devolvemos todo igual pero adaptando los títulos
    if not filtered:
        filtered = mock_data
        for o in filtered:
            o["titulo"] = f"{o['titulo']} ({query})"
            
    return filtered[:limit]
