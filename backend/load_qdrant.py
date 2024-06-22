from src.crawler import ImportedFileCrawler
from pathlib import Path
from src.encoder import ClipModel
from qdrant_client import QdrantClient
from src.database import Qdrant
from qdrant_client.models import Distance, VectorParams


data_path = Path(__file__).parent / "../data/products.json"
products_crawler = ImportedFileCrawler(data_path)
products_crawler.obtain_data()

clip_model = ClipModel()

qdrant_instance = QdrantClient("http://localhost:6333")
qdrant = Qdrant(qdrant_instance, clip_model, "Mori")
qdrant.client.recreate_collection(
            collection_name=qdrant.collection_name,
            vectors_config=VectorParams(size=512, distance=Distance.COSINE),
        )


products = products_crawler.get_data()

for i, product in enumerate(products):
    qdrant.set(product)
    if i >= 2000:
        break
    if i % 100 == 0:
        print(i)
print("finish")
