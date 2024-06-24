from meilisearch import Client

client = Client('http://127.0.0.1:7700', 'simple_password')

index = client.index('mori')
e = index.update_filterable_attributes(['name', 'region', 'current_price'])
# print(e)
filters = ['region = "QATAR"']
s = " AND ".join(filters)
print(s)

search_params = {
        'limit': 3,
        'filter': s,
}
search_result = index.search("" ,search_params)

print(search_result)