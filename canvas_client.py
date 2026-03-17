import httpx
from config import CANVAS_BASE_URL, CANVAS_TOKEN

API_URL = f"{CANVAS_BASE_URL}/api/v1"

HEADERS = {
    "Authorization": f"Bearer {CANVAS_TOKEN}",
    "Accept": "application/json",
}


async def canvas_get(endpoint: str, params: dict | None = None) -> list | dict:
    """Hace un GET a la API de Canvas y retorna el JSON."""
    url = f"{API_URL}/{endpoint.lstrip('/')}"
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()
