import json








arr = [13.13, 4.2, 12.124, 24.41]

arr2 = json.dumps(arr)


print(type(arr2))

print(json.loads(arr2))