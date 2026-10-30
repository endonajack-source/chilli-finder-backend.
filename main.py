from fastapi import FastAPI
from pydantic import BaseModel
import time

app = FastAPI()
server_database = {}

class ServerUpdate(BaseModel):
    job_id: str
    egg_name: str
    value: float
    rarity: str

@app.post("/update")
async def update_server_data(data: ServerUpdate):
    server_database[data.job_id] = {
        "egg_name": data.egg_name,
        "value": data.value,
        "rarity": data.rarity,
        "timestamp": time.time()
    }
    return {"status": "success"}

@app.get("/find-best")
async def find_best_server(min_value: float = 0.0, target_rarity: str = "Any"):
    current_time = time.time()
    best_server = None
    highest_value = -1.0
    
    for job_id, info in list(server_database.items()):
        if current_time - info["timestamp"] > 240:
            del server_database[job_id]
            continue
            
        if info["value"] >= min_value:
            if target_rarity == "Any" or info["rarity"].lower() == target_rarity.lower():
                if info["value"] > highest_value:
                    highest_value = info["value"]
                    best_server = {
                        "job_id": job_id,
                        "egg_name": info["egg_name"],
                        "value": info["value"],
                        "rarity": info["rarity"]
                    }
                    
    return best_server if best_server else {"job_id": None}
  
