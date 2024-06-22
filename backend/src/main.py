from typing import Union, Optional, List
from fastapi import FastAPI, HTTPException, Query, Depends
from crawler import ImportedFileCrawler
from pathlib import Path
from encoder import ClipModel
from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
from database import Qdrant
from pydantic import BaseModel
import os


app = FastAPI()

clip_model = ClipModel()

qdrant_host = os.environ.get('QDRANT_HOST', 'localhost')
qdrant_port = os.environ.get('QDRANT_PORT', '6333')

qdrant_instance = QdrantClient(qdrant_host, port=qdrant_port)
qdrant = Qdrant(qdrant_instance, clip_model, "Mori")


class SearchRequest(BaseModel):
    text: str 
    top: int 
    region: Optional[str] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    category: Optional[str] = None


class SearchResponse(BaseModel):
    id: str
    payload: dict

def parse_search_request(
    text: str = Query(...),
    top: int = Query(...),
    region: Optional[str] = Query(None),
    price_min: Optional[float] = Query(None),
    price_max: Optional[float] = Query(None),
    category: Optional[str] = Query(None)
) -> SearchRequest:
    return SearchRequest(text=text, top=top, region=region, price_min=price_min,
        price_max=price_max,
        category=category)


@app.get("/")
def read_root():
    return {"image": "salam"}


@app.get("/search/image/", )
def image_search(request: SearchRequest = Depends(parse_search_request)):
    # try:
        search_params = {
            "limit": request.top
        }
        filters = []

        if request.region:
            filters.append(
                FieldCondition(
                    key="region",
                    match=MatchValue(value=request.region)
                )
            )
        if request.price_min is not None and request.price_max is not None:
            filters.append(
                FieldCondition(
                    key="current_price",
                    range={"gte": request.price_min, "lte": request.price_max}
                )
            )
        elif request.price_min is not None:
            filters.append(
                FieldCondition(
                    key="current_price",
                    range={"gte": request.price_min}
                )
            )
        elif request.price_max is not None:
            filters.append(
                FieldCondition(
                    key="current_price",
                    range={"lte": request.price_max}
                )
            )
        if request.category:
            filters.append(
                FieldCondition(
                    key="category",
                    match=MatchValue(value=request.category)
                )
            )

        if filters:
            search_params["filter"] = Filter(must=filters)

        search_result = qdrant.get(text=request.text, search_params=search_params)
        response = [
            SearchResponse(id=point.id, payload=point.payload)
            for point in search_result
        ]
        return response
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)