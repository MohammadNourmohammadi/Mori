from typing import Union, Optional, List
from fastapi import FastAPI, HTTPException, Query, Depends
from encoder import ClipModel
from qdrant_client import QdrantClient
from database import Qdrant
from pydantic import BaseModel
import os
from meilisearch import Client
from database import Meilisearch
from starlette.responses import FileResponse


app = FastAPI()

text_top_search = os.environ.get('TEXT_SEARCH', 5)
image_top_search = os.environ.get('IMAGE_SEARCH', 6)

clip_model = ClipModel()

qdrant_host = os.environ.get('QDRANT_HOST', 'localhost')
qdrant_port = os.environ.get('QDRANT_PORT', '6333')

qdrant_instance = QdrantClient(qdrant_host, port=qdrant_port)
qdrant = Qdrant(qdrant_instance, clip_model, "Mori")

meili_host = os.environ.get('MEILI_HOST', 'http://localhost')
meili_port = os.environ.get('MEILI_PORT', '7700')

meili_instance = Client(f'{meili_host}:{meili_port}', 'simple_password')
meili_db = Meilisearch(meili_instance, "mori")


class SearchRequest(BaseModel):
    text: str 
    region: Optional[str] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    category: Optional[str] = None


class SearchResponse(BaseModel):
    id: str
    payload: dict

def parse_search_request(
    text: str = Query(...),
    region: Optional[str] = Query(None),
    price_min: Optional[float] = Query(None),
    price_max: Optional[float] = Query(None),
    category: Optional[str] = Query(None)
) -> SearchRequest:
    return SearchRequest(text=text, region=region, price_min=price_min,
        price_max=price_max,
        category=category)


def image_search(top:int, request: SearchRequest):
    # try:
        search_params = vars(request)
        search_params["top"] = top
        search_result = qdrant.get(text=request.text, search_params=search_params)
        response = [
            SearchResponse(id=point.id, payload=point.payload)
            for point in search_result
        ]
        return response
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))


def text_search(top:int, request: SearchRequest):
    params = vars(request).copy()
    params["top"] = top
    search_result = meili_db.get(text=request.text, params=params)
    response = [
        SearchResponse(id=str(point['id']), payload=point)
        for point in search_result["hits"]
    ]
    return response

@app.get("/search")
async def search(request: SearchRequest = Depends(parse_search_request)):
    image_response = image_search(image_top_search, request)
    text_response = text_search(text_top_search, request)
    image_response.extend(text_response)
    return image_response
   
templates_path = os.environ.get("TEMPLATES_PATH", './backend/src/templates/index.html')
@app.get("/")
async def read_index():
    return FileResponse(templates_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)
