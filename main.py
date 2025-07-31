from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import httpx

class YLINK(BaseModel):
    link:str
    lang:str


app=FastAPI()


@app.get("/")
async def root_check():
    return {"hello":"gaurav"}


@app.post("/api/generate-note")
async def api_generate_note(res: YLINK):
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.get(
            "https://api.supadata.ai/v1/transcript",
            params={"url": res.link, "text": True, "mode": "auto","lang": res.lang},
            headers={"x-api-key": "sd_0e8091de54d9b4cf3ab3a148aba3e341"}
        )
    # client is only available inside the block above
    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=r.text)
    data = r.json()
    return {"transcript": data.get("content"), "lang": data.get("lang")}