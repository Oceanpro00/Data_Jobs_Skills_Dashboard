# Import Dependencies
from flask import Flask, request, jsonify
from pymongo import MongoClient

# Initialize Flask App
app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["Cleaned_Job_Postings"]
collection = db["job_postings"]

# Define Home Route
@app.route('/')
def home():
    api_links = {
        "Machine Leaning Engineer": "/title_id/1",
        "Software & Platform Engineering": "/title_id/2",
        "Data Modeling & Warehousing": "/title_id/3",
        "Data Engineer": "/title_id/4",
        "Risk & Compliance Analytics": "/title_id/5",
        "Data Analyst": "/title_id/6",
        "MLOps Engineer": "/title_id/7",
        "Data Governance & Security": "/title_id/8",
        "Database Engineer / Administrator": "/title_id/9",
        "Data Scientist": "/title_id/10",
        "Data Architect": "/title_id/11",
        "Data Operations & Management": "/title_id/12",
        "Data Specialist": "/title_id/13",
        "Cloud & Infrastructure Engineering": "/title_id/14"
    }
    # Return the API links as a JSON response
    return jsonify(api_links)

# Define API Endpoints
@app.route('/title_id/<int:id>', methods=['GET'])
def classify_skill_hierarchy(id):
    # Validate the job_id input
    if not (1 <= id <= 14):
        return jsonify({"error": "Job ID must be a number between 1 and 14"}), 400
    
    # Define the aggregation pipeline
    pipeline = [
        
        # Stage 1: Match documents with the specified job_id
        {"$match": {"title_id": id}},
        
        # Stage 2: Lookup to join with job_titles collection
        {"$lookup": {
                "from": "title_classifications",  # The collection to join
                "localField": "title_id",         # Field from the job_postings
                "foreignField": "title_id",       # Field from the job_titles collection
                "as": "job_title_info"            # Output array field
            }
        },
        
        # Stage 3: Unwind the job_title_info array
        {"$unwind": "$job_title_info"},
        
        # Stage 4: Unwind the job_skills array
        {"$unwind": {"path": "$job_skills"}},
        
        # Stage 5: Group by skill and count occurrences of each skill
        {
            "$group": {
                "_id": "$job_skills",
                "count": {"$sum": 1},
                "job_classification": {"$first": "$job_title_info.job_classification"}
            }
        },
        
        # Stage 6: Sort the results by count in descending order
        {"$sort": {"count": -1}},
        
        # Stage 7: Limit the results to top 10 skills
        {"$limit": 10},
        
        # Stage 8: Project the final output format
        {
            "$project": {
                "_id": 0,
                "skill": "$_id",
                "count": 1,
                "job_classification": 1
            }
        }
    ]
    
    # Execute the aggregation pipeline
    results = list(collection.aggregate(pipeline))
    
    # Convert MongoDB documents to a JSON-friendly format
    top_skills = [{"skill": result["skill"], "count": result["count"]} for result in results]
    
    # Get the job_classification from the first document 
    if results:
        job_classification = results[0]["job_classification"]
    else:
        job_classification = None
    
    # Return the results
    return jsonify({
        "job_id": id,
        "job_classification": job_classification,
        "top_skills": top_skills
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)