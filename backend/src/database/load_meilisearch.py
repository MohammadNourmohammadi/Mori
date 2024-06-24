from src.crawler.imported_file_crawler import ImportedFileCrawler
from pathlib import Path
from meilisearch import Client

client = Client('http://127.0.0.1:7700', 'simple_password')

index = client.index('mori')



data_path = Path(__file__).parent / "data/products.json"
products_crawler = ImportedFileCrawler(data_path)
products_crawler.obtain_data()

products = products_crawler.get_data()


index.add_documents(products[:2000])
index.update_filterable_attributes(['name', 'region', 'current_price', 'category_name'])
print("Finish")
