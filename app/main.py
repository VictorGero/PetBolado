from typing import Union
import httpx
import json
from fastapi import FastAPI, Response

app = FastAPI()

OPENDOTA_API_BASE_URL = "https://api.opendota.com/api"

async def fetch_data(url: str, client: httpx.AsyncClient):
    response = await client.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch data from {url}", "status_code": response.status_code}

@app.get("/players/{account_id}")
async def get_player_details(account_id: int, response: Response):
    player_url = f"{OPENDOTA_API_BASE_URL}/players/{account_id}"
    recent_matches_url = f"{OPENDOTA_API_BASE_URL}/players/{account_id}/recentMatches"
    win_loss_url = f"{OPENDOTA_API_BASE_URL}/players/{account_id}/wl"

    async with httpx.AsyncClient() as client:
        player_data, recent_matches, win_loss = await asyncio.gather(
            fetch_data(player_url, client),
            fetch_data(recent_matches_url, client),
            fetch_data(win_loss_url, client)
        )

        if "error" in player_data:
            response.status_code = player_data.get("status_code", 500)
            return player_data

        combined_data = {
            "player_data": player_data,
            "recent_matches": recent_matches,
            "win_loss": win_loss
        }

        response.headers["Content-Type"] = "application/json"
        return combined_data
