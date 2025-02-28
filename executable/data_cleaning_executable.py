# %%
# Importing Dependencies
import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt

# %%
# Load the data
job_postings = pd.read_csv('../data/job_postings.csv')
job_skills = pd.read_csv('../data/job_skills.csv')

# %%
# Eliminate rows with null or missing values
cleaned_job_postings = job_postings.dropna()
cleaned_job_skills = job_skills.dropna()

# %%
# Eliminate unnecessary columns
columns_to_drop = ['last_status', 'got_summary', 'got_ner', 'is_being_worked', 'first_seen', 'job_type', 'search_city', 'search_position', 'job_level', 'search_country']
cleaned_job_postings = cleaned_job_postings.drop(columns=[col for col in columns_to_drop if col in cleaned_job_postings.columns])

# %%
# Fix last_processed_time 
cleaned_job_postings["last_processed_time"] = cleaned_job_postings["last_processed_time"].str.replace("+00", "+0000")


# %%
# Eliminate duplicate rows
columns_to_check = ['job_title', 'company', 'job_location']

cleaned_job_postings = cleaned_job_postings.drop_duplicates(subset=columns_to_check)


# %%
cleaned_job_postings[['City', 'State']] = cleaned_job_postings['job_location'].str.split(', ', n=1, expand = True)
cleaned_job_postings = cleaned_job_postings.drop(columns='job_location')

# %%
# Define a list of Valid US State Abbreviations
valid_states = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
]

# %%
# Remove all Rows that dont have the Standardized US State Abbreviations
cleaned_job_postings = cleaned_job_postings[cleaned_job_postings['State'].isin(valid_states)]

# %%
# target job title regex list
target_job_titles_regex = {
    "MLOps Engineer": r"(?i)(MLOps|Machine Learning Operations|Machine Learning Infrastructure Engineer|ML Infrastructure|ML Platform|ML Systems|ML Platform Engineer|AIML Ops Engineer|Machine Learning Software Developer)\w*[-\s]?",

    "Machine Learning Engineer": r"(?i)(Machine Learning Engineer|ML Engineer|Machine Learning Engineering|ML Developer|Machine Learning Software Engineer|AIML Engineer|AIML Data Scientist|AI Data Science Lead)\w*[-\s]?",

    "Data Architect": r"(?i)(Data Architect|Senior Data Architect|Cloud Data Architect|Big Data Architect|Enterprise Data Architect|Principal Data Architect|Lead Data Architect|Data Warehouse Architect|Data Architecture|Data Lake Architect|Data Streaming Architect)\w*[-\s]?",

    "Database Engineer / Administrator": r"(?i)(Database|Database Architect|DBA\b|Cloud Database|Azure Database|AWS Database|Databases|GCP Database|Oracle Database Engineer)\w*[-\s]?",

    "Data Engineer": r"(?i)(Data Engineer|Senior Data Engineer|Lead Data Engineer|Big Data Engineer|Data Engineering|Data Engineering Manager|Data Engineering Architect|Data Pipeline Engineer|Big Data Developer|Data Engineers|Data Integrations|Data Infrastructure|ETL Developer)\w*[-\s]?",

    "Data Governance & Security": r"(?i)(Data Governance|Data Privacy|Data Steward|Data Protection|Data Security|Master Data Management|Data Governance Manager|Data Compliance|Data Lifecycle Manager)\w*[-\s]?",

    "Data Operations & Management": r"(?i)(Data Manager|Enterprise Data Manager|Data Operations|Data Operations Manager|Data Operations Analyst|Data Management Engineer|Data Strategy Manager|Data Solution Architect|Data Deployment|Data Conversion|Data Replication Engineer|DevOps Engineer|Distributed Systems|Storage)\w*[-\s]?",

    "Data Modeling & Warehousing": r"(?i)(Data Modeling|Data Warehouse|Big Data Developer|Data Warehouse Architect|Cloud Datawarehouse|Data Platform Developer)\w*[-\s]?",

    "Data Specialist": r"(?i)(Data Specialist|Data Processing|Data Consultant|Data Quality Manager|Data Coordinator|Data Entry Specialist)\w*[-\s]?",

    "Data Scientist": r"(?i)(Data Scientist|Data Scientists|Data Science Engineer|Data Science Manager|Data Science Analyst|Data Science Practitioner|Customer Data Scientist)\w*[-\s]?",

    "Data Analyst": r"(?i)(Data Analyst|Data Analysts|Financial Data Analyst|Business Intelligence|BI Analyst|Data Business Analyst|Data Insights Analyst)\w*[-\s]?",

    "Software & Platform Engineering": r"(?i)(Software Engineer|Software Engineering|Software Developer|Software Engineer Data Science|Software Engineer Data Platforms|Platform Engineer|Application Developer|Backend Engineer|Systems Developer)\w*[-\s]?",

    "Cloud & Infrastructure Engineering": r"(?i)(Cloud Data|Cloud Data Architect|Azure Data|AWS Data|Azure Databricks|AWS Databricks|Cloud Engineer|Cloud Platform Engineer|Infrastructure Engineer|Datacenter Technician|Datacenter Engineer|Datacenter Network Engineer|Datacenter Engineering|Site Reliability Engineer|SRE)\w*[-\s]?",

    "Risk & Compliance Analytics": r"(?i)(Risk Analyst|AML\b|BSA|Risk Modeling|Financial Analyst|Hedge Fund|Data Loss Prevention|DLP)\w*[-\s]?"
}


# %%
# Function to Classify Job Titles
def classify(job_title, keywords_list=target_job_titles_regex):
    for industry, keyword in keywords_list.items():
        match = re.search(keyword, str(job_title))
        if match:
            keyword = re.sub(r'[^a-zA-Z\s]', '', match.group()).strip().title()   # using match.group() to return the actual keyword that was matched rather than the regex pattern
            return industry, keyword              
    return "unclassified", "unclassified"


# %%
# Copy Dataframe and Execute the classification function
classified_job_titles = cleaned_job_postings.copy()
classified_job_titles['job_classification'], classified_job_titles['job_keyword'] = zip(*classified_job_titles['job_title'].apply(classify))


# %%
# seniority level regex list
seniority_levels_regex = {
    # 🔹 Principal / Staff-Level Roles (Must Be Checked First)
    "Principal / Staff-Level": r"(?i)(Principal|Staff|Sr[-\s]?Staff|Distinguished|Fellow|Master|L4|Level 4|Chief[-\s]?Architect|Chief[-\s]?Scientist)\w*[-\s]?",

    # 🔹 Lead / Supervisor Roles (Checked Before Senior)
    "Lead": r"(?i)(Lead|Tech[-\s]?Lead|Team[-\s]?Lead|Supervisor|Group[-\s]?Lead|Project[-\s]?Lead|Engineering[-\s]?Lead|Squad[-\s]?Lead|Chapter[-\s]?Lead|Manager|Head[-\s]?of[-\s]?Team)\w*[-\s]?",

    # 🔹 Senior-Level Roles (Checked Before Mid-Level)
    "Senior-Level": r"(?i)(Senior|Sr\.?|SNR|SEN|L3|Level 3|Expert|Specialist|Advanced|Seasoned|Experienced)\w*[-\s]?",

    # 🔹 Mid-Level Roles (Checked Before Junior)
    "Mid-Level": r"(?i)(Mid[-\s]?Level|Intermediate|Mid|L2|Level 2|Professional|Regular)\w*[-\s]?",

    # 🔹 Entry-Level / Junior Roles (Checked After Principal & Senior)
    "Entry-Level / Junior": r"(?i)(Junior|Jr\.?|Entry[-\s]?Level|Associate|Graduate|Trainee|Fresher|New Grad|Early[-\s]?Career|L1|Level 1)\w*[-\s]?",

    # 🔹 Intern / Internship Roles (Checked Last)
    "Intern": r"(?i)(Intern|Internship|Co[-\s]?Op|Apprentice|Trainee)\w*[-\s]?",

    # 🔹 Director / Executive Roles (Checked Last for Highest Priority)
    "Director / Executive": r"(?i)(Director|Head|VP|Vice[-\s]?President|CIO|CTO|CISO|CEO|Chief|Executive|C[-]?Level|Managing[-\s]?Director|Global[-\s]?Head|President|Founder|Partner)\w*[-\s]?"
}


# %%
# Create single use function to classify seniority level
def classify_seniority_level(job_title):
    return classify(job_title, seniority_levels_regex)

# %%
# Execute the classification function on the copied dataframe
classified_job_titles['seniority_level'], classified_job_titles['seniority_level_keyword'] = zip(*classified_job_titles['job_title'].apply(classify_seniority_level))

# %%
# Create a For Loop and If Conditional to classify the unclassified seniority titles
for index, row in classified_job_titles.iterrows():
    if row['seniority_level'] == 'unclassified':
        if row['job_keyword'] == 'Data Analyst' or row['job_keyword'] == 'Data Security' or row['job_keyword'] == 'Database' or row['job_keyword'] == 'Cloud Engineer' or \
                row['job_keyword'] == 'Financial Data Analyst' or row['job_keyword'] == 'Bsa' or row['job_keyword'] == 'Machine Learning Engineer' or row['job_keyword'] == 'Data Processing' or \
                row['job_keyword'] == 'Backend Engineer' or row['job_keyword'] == 'Ml Engineering' or row['job_keyword'] == 'Data Governance' or row['job_keyword'] == 'Big Data Engineer' or \
                row['job_keyword'] == 'Aml' or row['job_keyword'] == 'Data Privacy' or row['job_keyword'] == 'Data Business Analyst' or row['job_keyword'] == 'Data Engineers' or \
                row['job_keyword'] == 'Data Engineer' or row['job_keyword'] == 'Infrastructure Engineer' or row['job_keyword'] == 'Datacenter Technician' or \
                row['job_keyword'] == 'Data Operations' or row['job_keyword'] == 'Data Science Engineer' or row['job_keyword'] == 'Data Consultant' or \
                row['job_keyword'] == 'Software Developer' or row['job_keyword'] == 'Data Science Analyst' or row['job_keyword'] == 'Bi Analyst' or \
                row['job_keyword'] == 'Ml Developer' or row['job_keyword'] == 'Ml Engineer' or row['job_keyword'] == 'Datacenter Engineer' or row['job_keyword'] == 'Platform Engineer' or \
                row['job_keyword'] == 'Cloud Data' or row['job_keyword'] == 'Etl Developer' or row['job_keyword'] == 'Dba' or row['job_keyword'] == 'Databases' or \
                row['job_keyword'] == 'Financial Analyst' or row['job_keyword'] == 'Devops Engineer' or row['job_keyword'] == 'Data Insights Analyst' or \
                row['job_keyword'] == 'Risk Analyst' or row['job_keyword'] == 'Data Analysts' or row['job_keyword'] == 'Cloud Database' or \
                row['job_keyword'] == 'Site Reliability Engineer' or row['job_keyword'] == 'Data Analystat' or row['job_keyword'] == 'Data Pipeline Engineer' or \
                row['job_keyword'] == 'Big Data Engineering':	
            classified_job_titles.loc[index, 'seniority_level'] = "Entry-Level / Junior" 
        elif row['job_keyword'] == 'Data Scientist' or row['job_keyword'] == 'Data Engineering' or row['job_keyword'] == 'MLOps Engineer' or \
                row['job_keyword'] == 'Business Intelligence' or row['job_keyword'] == 'Data Coordinator' or row['job_keyword'] == 'Data Steward' or \
                row['job_keyword'] == 'Machine Learning Infrastructure Engineer' or row['job_keyword'] == 'Machine Learning Software Developer' or row['job_keyword'] == 'Software Engineer' or \
                row['job_keyword'] == 'Customer Data Scientist' or row['job_keyword'] == 'Data Warehouse Architect'  or row['job_keyword'] == 'Ml Systems' or \
                row['job_keyword'] == 'Data Compliance' or row['job_keyword'] == 'Big Data Architect' or row['job_keyword'] == 'Aws Databricks' or \
                row['job_keyword'] == 'Big Data Developer' or row['job_keyword'] == 'Azure Data' or row['job_keyword'] == 'Data Replication Engineer' or \
                row['job_keyword'] == 'Data Science Practitioner' or row['job_keyword'] == 'Data Integrations' or row['job_keyword'] == 'Data Modeling' or \
                row['job_keyword'] == 'Machine Learning Operations' or row['job_keyword'] == 'Mlops' or row['job_keyword'] == 'Data Loss Prevention' or \
                row['job_keyword'] == 'Ml Infrastructure' or row['job_keyword'] == 'Machine Learning Software Engineer' or row['job_keyword'] == 'Data Deployment' or \
                row['job_keyword'] == 'Data Architecture' or row['job_keyword'] == 'Datacenter Network Engineer' or row['job_keyword'] == 'Azure Databricks' or \
                row['job_keyword'] == 'Data Stewardship' or row['job_keyword'] == 'Ml Platform' or row['job_keyword'] == 'Data Conversion' or \
                row['job_keyword'] == 'Data Management Engineer':
            classified_job_titles.loc[index, 'seniority_level'] = "Mid-Level"
        elif row['job_keyword'] == 'Data Architect' or row['job_keyword'] == 'Data Warehouse' or row['job_keyword'] == 'Cloud Data Architect' or \
                row['job_keyword'] == 'Data Protection' or row['job_keyword'] == 'Data Lake Architect' or row['job_keyword'] == 'Enterprise Data Architect' or \
                row['job_keyword'] == 'Data Solution Architect' or row['job_keyword'] == 'Data Streaming Architect':
            classified_job_titles.loc[index, 'seniority_level'] = "Senior-Level"



# %%
# Dropping rows
classified_job_titles = classified_job_titles[classified_job_titles['job_classification'] != 'unclassified']

# %%
# Classify job titles and create a new DataFrame with classification results
classified_job_titles['job_classification'], classified_job_titles['job_keyword'] = zip(*classified_job_titles['job_title'].apply(classify))

# Get unique job classifications and assign title_ids
unique_classifications = classified_job_titles[['job_classification']].drop_duplicates().reset_index(drop=True)
unique_classifications['title_id'] = range(1, len(unique_classifications) + 1)

# Get unique job keywords and assign keyword_ids
unique_keywords = classified_job_titles[['job_keyword']].drop_duplicates().reset_index(drop=True)
unique_keywords['keyword_id'] = range(1, len(unique_keywords) + 1)

# Merge the unique classifications back to the original DataFrame
classified_job_titles = pd.merge(classified_job_titles, unique_classifications, on='job_classification', how='left')

# Merge the unique keywords back to the original DataFrame
classified_job_titles = pd.merge(classified_job_titles, unique_keywords, on='job_keyword', how='left')

# %%
# Assign a unique identifier to each job posting\
classified_job_titles['job_id'] = [i for i in range(1, len(classified_job_titles) + 1)]

# %%
#Make the job_id the first column
column = ['job_id'] + [col for col in classified_job_titles.columns if col != 'job_id']
classified_job_titles = classified_job_titles[column]

# %%
# Output cleaned job postings data
classified_job_titles.to_csv('../data/cleaned_job_postings.csv', index=False)

# Output cleaned job skills data 
job_skills.to_csv('../data/cleaned_job_skills.csv', index=False)

print("CSV files successfully exported to data directory")



