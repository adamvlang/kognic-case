import json

from fastapi import FastAPI, Request
from annotation_convertion.kognic_to_openlabel import convert
from pydantic import BaseModel

app = FastAPI()

@app.post("/kognic_to_openlabel")
async def convert_kognic_to_openlabel(request: Request):
  body = await request.body()
  return json.loads(convert(json.loads(body)))
