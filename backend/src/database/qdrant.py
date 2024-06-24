from typing import List, Union
from encoder import Encoder
from database.abstract import VectorDatabase
from qdrant_client import QdrantClient, models
import PIL
import uuid
from qdrant_client.http.models import Filter, FieldCondition, MatchValue

class Qdrant(VectorDatabase):

    def __init__(self, db_instance: QdrantClient, encoder: Encoder, collection_name: str) -> None:
        super().__init__(encoder)
        self.client = db_instance
        self.collection_name = collection_name

    def set(self, product: dict):
        images = product["images"]
        vectors = [self.encoder.encode_image(image) for image in images]

        for i, vector in enumerate(vectors):
            unique_id = str(uuid.uuid4())
            payload = {"image_number": i}
            payload.update(product)
            payload["product_id"] = payload.pop("id")

            self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    {
                        "id": unique_id,
                        "vector": vector,
                        "payload": payload
                    }
                ]
            )

    def get(self, text: str, search_params:dict):
        filters = self._get_filter(search_params)
        query_vector = self.encoder.encode_text(text)
        search_result = self.client.search(
            collection_name = self.collection_name,
            query_vector = query_vector,
            limit = search_params["top"],
            with_payload = True,
            query_filter = filters
        )
        return search_result
    
    def _get_filter(self, params:dict):

        search_params = {}
        filters = []

        if params['region']:
            filters.append(
                FieldCondition(
                    key="region",
                    match=MatchValue(value=params['region'])
                )
            )
        if params['price_min'] is not None and params['price_max'] is not None:
            filters.append(
                FieldCondition(
                    key="current_price",
                    range={"gte": params['price_min'], "lte": params['price_max']}
                )
            )
        elif params['price_min'] is not None:
            filters.append(
                FieldCondition(
                    key="current_price",
                    range={"gte": params['price_min']}
                )
            )
        elif params['price_max'] is not None:
            filters.append(
                FieldCondition(
                    key="current_price",
                    range={"lte": params['price_max']}
                )
            )
        if params['category']:
            filters.append(
                FieldCondition(
                    key="category_name",
                    match=MatchValue(value=params['category'])
                )
            )

        if filters:
            return Filter(must=filters)
        else:
            return {}


