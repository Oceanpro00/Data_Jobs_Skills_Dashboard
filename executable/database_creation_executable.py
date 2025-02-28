# %%
# Insert Dependencies
import json
from pymongo import MongoClient

# %%
# Connect to MongoDB
# Update if using a remote MongoDB
client = MongoClient("mongodb://localhost:27017/") 

# %%
# Create/Connect to the database
db = client["Cleaned_Job_Postings"]

# %%
# Load the JSON file into a Python object
files = ["title_classifications", "keyword_classifications", "job_postings"]

for file in files:
    
    # Create/Connect to the collection then drop it once
    collection = db[file]
    collection.drop()
    
    with open("../data/" + file + ".json") as f:
        file_data = json.load(f)
    
    # Insert data into MongoDB
    if isinstance(file_data, list):  # If JSON is an array
        collection.insert_many(file_data)
    else:  # If JSON is a single document
        collection.insert_one(file_data)


