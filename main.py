import uvicorn
from fastapi import FastAPI, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List


class Account(BaseModel):
    name: str
    id: int

class Accounts(BaseModel):
    accounts: List[Account]

class Song(BaseModel):
    name: str
    album: str
    artist: str

class Songs(BaseModel):
    songs: List[Song]

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

memory_db = {"accounts": [], "songs": []}

@app.get("/accounts", response_model=Accounts)
def get_accounts():
    return {"accounts": memory_db["accounts"]}

@app.post("/accounts", response_model=Accounts)
def add_accounts(account: Account):
    memory_db["accounts"].append(account)
    return {"accounts": memory_db["accounts"]}

@app.delete("/accounts/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(account_id : int):
    for index, account in enumerate(memory_db["accounts"]):
         if account.id == account_id:
            del memory_db["accounts"][index]
            return Response(status_code=status.HTTP_204_NO_CONTENT)
         
    raise HTTPException(status_code=404, detail="Account not found")
    
@app.get("/songs", response_model=Songs)
def get_songs():
    return {"songs": memory_db["songs"]}

@app.post("/songs", response_model=Songs)
def add_songs(song: Song):
    memory_db["songs"].append(song)
    return {"songs": memory_db["songs"]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
