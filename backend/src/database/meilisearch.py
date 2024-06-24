from database.abstract import TextDatabase
import meilisearch 

class Meilisearch(TextDatabase):

    def __init__(self, db_instance: meilisearch.Client, index: str) -> None:
        super().__init__()
        self.db = db_instance
        self.index = self.db.index(index)
    
    def set(self, product: dict):
        self.index.add_documents([product])
    
    def get(self, text: str, params:dict):
        filter = self._create_filter(params)
        search_params = {
        'limit': params["top"],
        'filter': filter,
        }
        search_result = self.index.search(text ,search_params)
        return search_result

    def _create_filter(self, params: dict) -> str:
        filters = []
        if params["region"]:
            filters.append("region = " + params["region"])
        if params["category"]:
            filters.append("category_name = " + params["category"])
        if params['price_min']: 
            filters.append("current_price > " + str(params["price_min"]))
        if params['price_max']:
            filters.append("current_price < " + str(params["price_max"]))
        
        return " AND ".join(filters)
