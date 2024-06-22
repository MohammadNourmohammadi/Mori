from typing import List, Union
from encoder import Encoder
from database.abstract import VectorDatabase
from qdrant_client import QdrantClient, models
import PIL
import uuid

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
        filters = search_params.get("filter", {})
        query_vector = self.encoder.encode_text(text)
        search_result = self.client.search(
            collection_name = self.collection_name,
            query_vector = query_vector,
            limit = search_params["limit"],
            with_payload = True,
            query_filter = filters
        )
        return search_result


