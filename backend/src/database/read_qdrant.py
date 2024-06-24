import requests

base_url = "http://localhost:6333"
collection_name = "Mori"
offset = 0
limit = 100

all_points = [] 

response = requests.post(
    f"{base_url}/collections/{collection_name}/points/scroll",
    headers={"Content-Type": "application/json"},
    json={
        "limit": 700,
        "with_payload": True,
        "with_vector": True
    }
)

data = response.json()
points = data.get('result', {}).get('points', [])

all_points.extend(points)

print(len(all_points))
# print(all_points)
# for point in all_points:
#     print(f"ID: {point['id']}, Vector: {point['vector']}, Payload: {point.get('payload', {})}")

# print(all_points[0])
