# %%
# Importing Dependencies
import pandas as pd
import re
import json
from datetime import datetime


# %%
# Load in the Datasets
job_postings = pd.read_csv('../data/cleaned_job_postings.csv')
job_skills = pd.read_csv('../data/cleaned_job_skills.csv')

# %%
# Merge left on job_postings and job_skills on the 'job_link' column
merged_data = job_postings.merge(job_skills, on='job_link', how='left')

# Drop the 'job_link' column
merged_data = merged_data.drop(columns=['job_link'])

# %%
# Split the job_skills column into a list of skills
merged_data['job_skills'] = merged_data['job_skills'].str.split(', ')

# %%
# Explode the Split job_skills
skill_breakdown = merged_data.explode('job_skills')

# Remove any Null or Empty Skills
skill_breakdown = skill_breakdown.dropna(subset=['job_skills'])
skill_breakdown = skill_breakdown[skill_breakdown['job_skills'] != '']

# %%
# Function to dynamically map skills based on keywords
def dynamic_skill_mapping(skill):

    # Standardizing Education-Related Skills

    bachelor_variations = [
        "bachelor of", "bachelor's", "ba", "bs", "b.a.", "b.s.",
        "bachelor", "bachlor", "bacs", "bsc", "b.sc."
    ]
    
    master_variations = [
        "master of", "master's", "ma", "ms", "m.a.", "m.s.",
        "master", "mphil", "m.phil.", "mpa", "m.p.a.", "msc", "m.sc."
    ]
    
    phd_variations = [
        "phd", "doctorate", "doctor of philosophy", "doctor's degree",
        "ph.d.", "phd.", "dr", "dr.", "doctor"
    ]

    for variation in bachelor_variations:
        if variation in skill:
            return "bachelor's degree"
    
    for variation in master_variations:
        if variation in skill:
            return "master's degree"
    
    for variation in phd_variations:
        if variation in skill:
            return "phd"

    # Grouping AWS Certifications into Categories
    if "aws cloud practitioner" in skill:
        return "AWS Fundamentals"
    if "developer" in skill and "aws" in skill:
        return "AWS Developer Certifications"
    if "architect" in skill and "aws" in skill:
        return "AWS Architecture Certifications"
    if "devops" in skill and "aws" in skill:
        return "AWS DevOps Certifications"
    if "sysops" in skill and "aws" in skill:
        return "AWS SysOps Administrator"
    
    # Standardizing Data Science & Machine Learning Skills
    if "machine learning" in skill or "ml engineer" in skill:
        return "machine learning"
    if "deep learning" in skill:
        return "deep learning"
    if "natural language processing" in skill or "nlp" in skill:
        return "natural language processing"

    # Cloud & Infrastructure Skills
    if "gcp" in skill or "google cloud" in skill:
        return "Google Cloud Platform"
    
    # Business Intelligence & Data Analysis
    if "power bi" in skill:
        return "Power BI"
    if "tableau" in skill:
        return "Tableau"
    if "excel" in skill or "spreadsheet" in skill:
        return "Excel"
    
    # Programming Languages
    if "python" in skill:
        return "Python"
    if "r programming" in skill or skill == "r":
        return "R Programming"
    if "java" in skill:
        return "Java"
    if "javascript" in skill or "js" in skill:
        return "JavaScript"
    if "c++" in skill or "c plus plus" in skill:
        return "C++"

    # Databases
    if "postgresql" in skill or "postgre" in skill:
        return "PostgreSQL"
    if "mongodb" in skill:
        return "MongoDB"
    
    if "$" in skill or "hour" in skill or "day" in skill:
        return None
    
    if "relevant" in skill or "related" in skill:
        return None

    if "24/7" in skill or "24x7" in skill:
        return None

    if "401k" in skill or "401(k)" in skill or "retirement" in skill:
        return None   
    
    if "*" in skill:
        return skill[1:].strip()
    
    if "'big data'" in skill:
        return "big data"
    
    if "years experience" in skill or "years of experience" in skill or "years'" in skill or "year of" in skill or "year" in skill:
        return None
    
    if "a/b" in skill:
        return "a/b testing"
    
    if "ability" in skill:
        return None
    
    if "bsa" in skill:
        return "bsa/aml"
    
    if "data engineering" in skill:
        return "data engineering"
    
    if "data entry" in skill:
        return "data entry"
    
    if "etl" in skill:
        return "ETL"

    # Default: Return skill as is if no match is found
    return skill



# %%
# Standardize job_skills to lowercase and remove extra spaces
skill_breakdown["lowercase_skills"] = skill_breakdown["job_skills"].str.lower().str.strip()

# Apply the dynamic skill mapping function to the unique skills list
cleaned_unique_skills = [dynamic_skill_mapping(skill) for skill in skill_breakdown["lowercase_skills"]]

# %%
# Replace the job_skills column with the cleaned skills
skill_breakdown["job_skills"] = cleaned_unique_skills

# Drop the lowercase_skills column
skill_breakdown = skill_breakdown.drop(columns=["lowercase_skills"])

# Drop Null or Empty Rows
skill_breakdown = skill_breakdown.dropna(subset=['job_skills'])


# %%
# Skill Normalization by Ranking Priority
skill_normalization = {
    
    # Classification Control to limit clash of the multiple Skill Standardizations (Refer to Jose's Section)
    
    "bachelor's degree": r"(?i)\bbachelor's degree\b",
    "master's degree": r"(?i)\bmaster's degree\b",
    "phd": r"(?i)\bphd\b",
    "AWS Fundamentals": r"(?i)\bAWS Fundamentals\b",
    "AWS Developer Certifications": r"(?i)\bAWS Developer Certifications\b",
    "AWS Architecture Certifications": r"(?i)\bAWS Architecture Certifications\b",
    "AWS DevOps Certifications": r"(?i)\bAWS DevOps Certifications\b",
    "AWS SysOps Administrator": r"(?i)\bAWS SysOps Administrator\b",
    
    # Cloud & Infrastructure Engineering:
    
    "Troubleshooting": r"(?i)troubleshooting",
    "Linux": r"(?i)linux",
    "Communication": r"(?i)communication|communication\s+skills|comm|comms|communicate",
    "Cabling": r"(?i)cable[-\s]*ing",
    "Networking": r"(?i)networking",
    "Data Center Operations": r"(?i)data\s+center\s+operations",
    "Windows": r"(?i)windows",
    "Azure Data Factory": r"(?i)azure\s+data\s+factory|azuredatafactory",
    "Terraform": r"(?i)terraform",
    "Bash": r"(?i)(bash|shell|command\s+line|cli)",
    "Big Data": r"(?i)big\s+data|bigdata",
    "Data Engineering": r"(?i)data\s+engineering|dataeng|data\sengg|data\sengr",
    "Databricks": r"(?i)databricks",
    "Go": r"(?i)go|golang",
    "Inventory Management": r"(?i)inventory\s+management|inv\s+mgmt|inv\s+mgmnt",
    
    # Data Analyst:
    
    "Data Analysis": r"(?i)data\s*(analysis|analytics)|data\s*analyse",
    "Tableau": r"(?i)tableau",
    "Data Visualization": r"(?i)data\s+visualization|data\s+visualisation",
    "Excel": r"(?i)excel",
    "Power BI": r"(?i)power\s*bi",
    "Statistics": r"(?i)statistics|statistical",
    "Reporting": r"(?i)reporting|reports",
    "Teamwork": r"(?i)teamwork|collaboration|team-\s*first\s*mentality",
    "Data Mining": r"(?i)data\s+mining|mining",
    "Problem Solving": r"(?i)problem\s+solving|troubleshooting",
    "Business Intelligence": r"(?i)business\s*intelligence|bi",
    "Project Management": r"(?i)project\s*management",
    "Data Management": r"(?i)data\s+management",
    
    # Data Architect:
    
    "Data Architecture": r"(?i)data\s*(architecture|architect)",
    "Data Modeling": r"(?i)data\s*modeling|data\s*models|data\s*design",
    "Data Warehousing": r"(?i)data\s*warehousing|data\s*marts|dw",
    "Data Governance": r"(?i)data\s*governance|data\s*policy|data\s*compliance",
    "Snowflake": r"(?i)snowflake",
    "Data Integration": r"(?i)data\s*integration|etl|extract\s+transform\s+load|data\s*flow",
    "Data Quality": r"(?i)data\s*quality|dq",
    "Hadoop": r"(?i)hadoop",
    "Data Security": r"(?i)data\s*security|data\s*protection|cybersecurity",
    "ETL": r"(?i)etl|extract\s+transform\s+load|data\s*flow",
    "NoSQL": r"(?i)nosql",
    
    #Data Engineer:
    
    "Spark": r"(?i)spark|apache\s+spark",
    "Scala": r"(?i)scala",
    "Kafka": r"(?i)kafka|apache\s+kafka",
    "Redshift": r"(?i)redshift|amazon\s+redshift",
    "NoSQL": r"(?i)nosql",
    "Hive": r"(?i)hive|apache\s+hive",
    "ETL": r"(?i)etl|extract\s+transform\s+load",
    "MySQL": r"(?i)mysql",
    "Agile": r"(?i)agile",
    "EMR": r"(?i)emr|elastic\s+mapreduce|amazon\s+emr",
    "Airflow": r"(?i)airflow|apache\s+airflow",
    "Cassandra": r"(?i)cassandra|apache\s+cassandra",
    
    # Data Governance & Security:
    
    "Data Governance": r"(?i)data\s*governance|dg",
    "Data Privacy": r"(?i)data\s+privacy",
    "Analytical Skills": r"(?i)analytical\s+skills",
    "Computer Science": r"(?i)computer\s+science|cs",
    "Data Protection": r"(?i)data\s+protection|data\s*prot|dp",
    "Data Stewardship": r"(?i)data\s*stewardship",
    "GIS": r"(?i)gis|geographic\sinformation\s+systems",
    "GDPR": r"(?i)gdpr|general\+data\s+protection\s+regulation",
    
    # Data Modeling and Warehousing:
    
    "JSON": r"(?i)json",
    "SPARQL": r"(?i)sparql",
    "AVRO": r"(?i)avro",
    "Ontology": r"(?i)ontology",
    "OpenAPI/YAML": r"(?i)openapi/yaml",
    "OWL": r"(?i)owl",
    "SKOS": r"(?i)skos",
    "Data.World": r"(?i)data\.world",
    "RDFS": r"(?i)rdfs",
    "Stardog": r"(?i)stardog",
    "AnzoGraph": r"(?i)anzograph",
    "Neptune": r"(?i)neptune",
    "PoolParty": r"(?i)poolparty",
    
    # Data Operations & management: engineering
    
    'Collaboration': r"(?i)collaboration",
    'Attention to Detail': r"(?i)attention\s*to\s*detail",\
    'Microsoft Office Suite': r"(?i)microsoft\s*office(?:\ssuite)?",
    'Data Validation': r"(?i)data\s*validation",
    
    # Data Scientist:
    
    'Data Science': r"(?i)data\s*science",
    'Machine Learning': r"(?i)machine\s*learning|ml",
    'Mathematics': r"(?i)mathematics|maths",
    'PyTorch': r"(?i)pytorch",
    
    # Data Specialist:
    
    'Data Entry': r"(?i)data\s*entry",
    'Multitasking': r"(?i)multitasking",
    
    # Data Engineer / Administrator:
    
    'Oracle': r"(?i)oracle",
    'Database Administration': r"(?i)database\s*administration|db\sa|dba",
    'SQL Server': r"(?i)sql\s*server",
    'PostgreSQL': r"(?i)postgresql|postgres",
    'Database Design': r"(?i)database\sgesign|db\sdesign|database\sstructure",
    'PL/SQL': r"(?i)pl/sql",
    'MongoDB': r"(?i)(mongodb|mongo\s*database)",
    'Performance Tuning': r"(?i)performance\stuning|tuning",
    
    # ML Ops Engineer:
    
    'Reinforcement Learning': r"(?i)reinforcement\s*learning",
    'Probabilistic Graphs': r"(?i)probabilistic\s*graphs",
    'Flexibility': r"(?i)flexibility",
    'NLP': r"(?i)(nlp|natural\s*language\s*processing)",
    'Monitoring': r"(?i)monitoring",
    'Autonomy': r"(?i)autonomy",
    'Experimentation': r"(?i)experimentation",
    'Deep Learning': r"(?i)deep\s*learning",
    'ML Ops': r"(?i)(ml\s*ops|mlops|machine\s*learning\s*operations)",
    'Workflow Orchestration': r"(?i)workflow\s*orchestration",
    'Product Ownership': r"(?i)product\s*ownership",
    
    # Machine Learning Engineer:
    
    'TensorFlow': r"(?i)(tensorflow|tensor\s*flow)",
    'Pandas': r"(?i)pandas",
    'Data Preparation': r"(?i)data\s*preparation",
    'Jupyter': r"(?i)jupyter",
    'Numba': r"(?i)numba",
    "Cloud Computing": r"(?i)cloud\s+computing|cc",
    'Model Deployment': r"(?i)model\s*deployment",
    "Kubernetes": r"(?i)kubernetes|kube",
    'Docker': r"(?i)docker",
    'Feature Engineering': r"(?i)feature\s*engineering",
    
    # Risk and Compliance Analyst:
    
    'CISM': r"(?i)(certified\s*information\s*systems\s*manager|cism)",
    'JIRA': r"(?i)jira",
    'CISSP': r"(?i)(certified\s*information\s*systems\s*security\s*professional|cissp)",
    'CCSP': r"(?i)(certified\s*cloud\s*security\s*professional|ccsp)",
    'CISA': r"(?i)(certified\s*information\s*systems\s*auditor|cisa)",
    'Security+': r"(?i)(comp\.?\s*tia\ssecurity\+\s*certification|security\+)",
    'GIAC': r"(?i)giac",
    'AWS Cloud Practitioner': r"(?i)(aws\s*cloud\s*practitioner|awscp)",
    'AWS Solution Architect Associate': r"(?i)(aws\s*solution\s*architect\s*associate|aws\ssaa)",
    'AWS Solution Architect Professional': r"(?i)(aws\s*solution\s*architect\s*professional|aws\sasap)",
    'AWS Developer Associate': r"(?i)(aws\s*developer\s*associate|aws\sdaa)",
    'AWS Security Specialty': r"(?i)(aws\s*security\s*specialty|awsss)",
    'Virtualization': r"(?i)virtualization",
    'Cybersecurity': r"(?i)cybersecurity",
    'Data Loss Prevention (DLP)': r"(?i)(data\s*loss\s*prevention|dlp)",
    'Network DLP': r"(?i)(network\s*dlp|ndlp)",
    'SaaS': r"(?i)saas",
    
    # Software and Platform Engineering:
    
    "Software Engineering": r"(?i)software\s+engineering",
    "Kafka": r"(?i)kafka",
    "C++": r"(?i)c\+\+|\bCPLUSPLUS\b",
    "Algorithms": r"(?i)algorithms|algo",
    "CI/CD": r"(?i)ci/cd|continuous\s+integration/\s*continuous\s+deployment",
    "AI": r"(?i)ai|artificial\s+intelligence",
    
    # General / Added:
    
    'Engineering': r"(?i)engineering",
    'LLMs': r"(?i)(llms|large\s*language\s*models)",
    "Python": r"(?i)python(?:3(\.\d+)?)?|py",
    "RDF": r"(?i)rdf",
    "AWS": r"(?i)aws|amazon\s+web\sservices",
    "SQL": r"(?i)sql",
    "Azure": r"(?i)azure|microsft\s+azure",
    "Java": r"(?i)java|java\s+ee|java\s+se",
    "R": r"(?i)(?:^|[\s,])(r(?:\s+(?:programming|language|studio|basics|core|developer|development|statistical|stats|analysis))?)\b"
    
}

# %%
# Function To Standardize top 20 Skills by Job Classification
def classify(skill):
    for skill_name, keyword in skill_normalization.items():
        if re.search(keyword, skill):
            return skill_name
    return skill

# %%
# Apply Regex Function to skill_breakdown Dataframe
skill_breakdown['job_skills'] = skill_breakdown['job_skills'].apply(classify)


# %%
# Remove duplicate job_skills per job_id, keeping only the first occurrence
unique_skills_df = skill_breakdown.drop_duplicates(subset=["job_id", "job_skills"])

# %%
result_df = unique_skills_df.groupby(['job_id', 'last_processed_time', 'job_title', 'company', 'City', 'State', 'title_id',
                        'job_classification', 'keyword_id', 'job_keyword', 'seniority_level', 'seniority_level_keyword'], as_index=False).agg(
    job_skills=('job_skills', list)
)

# %%
# Split CSV into 3 files
title_classifications_df = result_df[['title_id', 'job_classification']].drop_duplicates(subset='title_id')
keyword_classifications_df = result_df[['keyword_id', 'job_keyword']].drop_duplicates(subset='keyword_id')
job_postings_df = result_df[['job_id', 'last_processed_time', 'job_title', 'company', 'City', 'State', 'title_id', 'keyword_id', 'seniority_level', 'seniority_level_keyword', 'job_skills']]

# %%
# Convert the result_df into a job_postings_json, title_classifications_json, and keyword_classifications_json
title_classifications_json = json.loads(title_classifications_df.to_json(orient='records'))
keyword_classifications_json = json.loads(keyword_classifications_df.to_json(orient='records'))
job_postings_json = json.loads(job_postings_df.to_json(orient='records'))

# %%
# Save JSON to a file
with open("../data/title_classifications.json", "w") as json_file:
    json_file.write(json.dumps(title_classifications_json, indent=4))
print("title_classifications CSV has been converted to JSON successfully!")    

with open("../data/keyword_classifications.json", "w") as json_file:
    json_file.write(json.dumps(keyword_classifications_json, indent=4))
print("keyword_classifications_json CSV has been converted to JSON successfully!")    

with open("../data/job_postings.json", "w") as json_file:
    json_file.write(json.dumps(job_postings_json, indent=4))
print("job_postings_json CSV has been converted to JSON successfully!")    


