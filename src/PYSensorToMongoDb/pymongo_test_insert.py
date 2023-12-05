# Get the database using the method we defined in pymongo_test_insert file
from PYmongoGetDatabase import get_database
dbname = get_database()
collection_name = dbname["sensorstate"]

item_1 = {
  "timestamp" : "13.34",
  "payload" : "on",
}


collection_name.insert_one(item_1)