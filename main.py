from typing import Union
import httpx
import json
from fastapi import FastAPI, Response

app = FastAPI()

# URL base da API do OpenDota
OPENDOTA_API_BASE_URL = "https://api.opendota.com/api"


@app.get("/players/{account_id}")
async def get_player_details(account_id: int, response: Response):
    url = f"{OPENDOTA_API_BASE_URL}/players/{account_id}"
    
    async with httpx.AsyncClient() as client:
        response_opendota = await client.get(url)
        if response_opendota.status_code == 200:
            player_data = response_opendota.json()
            response.headers["Content-Type"] = "application/json"
            return player_data
        else:
            response.status_code = response_opendota.status_code
            return {"error": "Player not found"}

