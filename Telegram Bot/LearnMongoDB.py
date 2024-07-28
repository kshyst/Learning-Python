from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

db = client['qdatabase']

collection = db['qcollection']

user1 = {'name': 'SAliB', 'age': 30, 'email': 'salib@example.com'}
user2 = {'name': 'Bagher', 'age': 25, 'email': 'bagher@example.com'}

result = collection.insert_one(user1)
print('Inserted id:', result.inserted_id)

result = collection.insert_many([user2])
print('Inserted ids:', result.inserted_ids)

print('All users:')
for user in collection.find():
    print(user)

print('User with name Bagher:')
print(collection.find_one({'name': 'Bagher'}))

collection.update_one({'name': 'SAliB'}, {'$set': {'age': 35}})
print('User with name SAliB:')
print(collection.find_one({'name': 'SAliB'}).get('age'))

print()
print()
print()
print()

results = collection.aggregate([{"$sort": {"age": -1}}, {"$limit": 10}])
for document in results:
    print(document)
