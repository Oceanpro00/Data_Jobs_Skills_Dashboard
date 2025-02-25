# Data Employment Skills Dashboard

## Repository Overview

This repository contains the codebase for the **Data Career Skills Dashboard**, an interactive tool designed to help job seekers identify and prioritize the most in-demand skills for 14 of the most commonly and most representative posted Data Science job categorizations. The dataset is limited to the United States and only includes job categories that had at least 50 - 100 job listings posted within the year 2014.

Users will be able to:

- Select one of the **14 Data Career Categorizations**.
- View a **breakdown of relevant skills** for that category.
- Dynamically **adjust skill ranking** based on designated skills they already possess.

The project focuses on delivering an **MVP (Minimum Viable Product)** that provides actionable insights, albeit in a limited and general scope, due to time constraints.

## Project Team

- **Sean Schallberger**
- **Jose Traboulsi**
- **Karla Lopez**
- **Meghdut Noor**

## Dataset & Legal Considerations

We source data from the following:

- **Data Science Job Postings & Skills (2024)**  
  [Dataset Link](https://www.kaggle.com/datasets/asaniczka/data-science-job-postings-and-skills?select=job_postings.csv)

The dataset has been cleaned, standardized, and transformed to improve usability based on exploratory data analysis.

### Legal Considerations

The dataset is provided under the **Open Data Commons Attribution License (ODC-By) v1.0**, which allows for free use, sharing, and modification of the data, provided proper attribution is given.  

## Project Structure

### 1. Data Pipeline Overview

📂 **Data Sources:**  
- `job_postings.csv` → Contains job titles, descriptions, locations, etc.  
- `job_skills.csv` → Contains extracted skills from job postings.  

📂 **Exploratory Data Analysis (EDA):**  
- **EDA 1.1:** Initial data classification and job categorization.  
- **EDA 1.2:** Location-based job market analysis.  
- **EDA 1.3:** Ethical bias assessment and dataset limitations.  

The EDA process guided the **data cleaning and job standardization process**, and due to its exploratory nature, it was split among individual team members.

📂 **Data Cleaning Process:** (`data_cleaning.py`)
- Standardizes job titles and maps experience levels.
- Removes duplicates and filters irrelevant postings.
- Outputs a structured dataset for skill extraction.

📂 **Skill Extraction Process:** (`skill_extraction.py`)
- Maps skills to job titles and experience levels.
- Normalizes skill names using regex-based standardization.
- Groups and ranks skills based on demand.

📂 **Database Creation & Storage:** (`database_creation.py`)
- Stores cleaned job and skill data in **MongoDB**.
- Ensures efficient indexing and fast query retrieval.

📂 **Dashboard Development (Frontend & API):**
- Uses **Flask/FastAPI** to serve data dynamically.
- Develops **JavaScript-based visualizations** with interactive ranking & filtering.
- Enables users to compare their skills with industry demands.

## Steps to Reproduce Results

1. **Clone the repository:**
   ```sh
   git clone https://github.com/your-repo-url.git
   cd Data_Career_Skills_Dashboard
   ```

2. **Install required dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Run Data Cleaning & Skill Extraction:**
   ```sh
   python data_cleaning.py
   python skill_extraction.py
   ```

4. **Load cleaned data into MongoDB:**
   ```sh
   python database_creation.py
   ```

5. **Run Flask API:**
   ```sh
   python api_endpoints.py
   ```

6. **Launch the Frontend Dashboard:**
   Open `index.html` in your browser.

## Sprint Breakdown & Key Features

### **Sprint 1: Data Collection & Cleaning**
- Load datasets and evaluate job market representation.
- Standardize job titles and experience levels.
- Remove duplicates and irrelevant job postings.
- Assess dataset biases and ethical concerns.

### **Sprint 2: Skill Processing**
- Extract skills from job postings and structure them.
- Rank and categorize skills by demand and relevance.

### **Sprint 3: Database & API Development**
- Upload processed job and skill data to **MongoDB**.
- Develop API endpoints for **dynamic skill retrieval and recommendations**.

### **Sprint 4: Dashboard Development**
- Build an **interactive skill ranking dashboard** using JavaScript.
- Implement **search, filtering, and user customization features**.

## Repository File Structure

```
Data_Career_Skills_Dashboard/
│── data/                      # Datasets
│   ├── job_postings.csv       # Raw job postings dataset
│   ├── job_skills.csv         # Raw skills dataset
│   ├── cleaned_data.csv       # Processed dataset (after cleaning)
│
│── backend/                   # API for data retrieval & recommendations
│   ├── api_endpoints.py       # Flask API for job skills & recommendations
│
│── frontend/                   # Interactive dashboard
│   ├── index.html             # Main UI (calls dashboard_visuals.js)
│   ├── dashboard_visuals.js   # JavaScript visuals for skill rankings
│
│── notebooks/                 # Jupyter notebooks for data processing
│   ├── eda_1.1_classification_exploration.ipynb
│   ├── eda_1.2_location_splitting.ipynb
│   ├── eda_1.3_ethical.ipynb
│   ├── data_cleaning.ipynb
│   ├── skill_extraction.ipynb
│   ├── database_creation.ipynb
│
│── README.md                  # Project documentation
│── requirements.txt           # Dependencies
│── .gitignore                 # Ignore unnecessary files
```

## Final Deliverables
✅ **Interactive Dashboard** with job skill insights.  
✅ **MongoDB Database** storing cleaned job postings and skill data.  
✅ **Flask API** serving skill recommendations dynamically.  
✅ **GitHub Repository** with fully documented code.  
✅ **Project Presentation Deck** summarizing key insights.  

## Contribution Guidelines

1. **Fork the repository and create a feature branch:**
   ```sh
   git checkout -b feature-name
   ```

2. **Commit and push your changes:**
   ```sh
   git commit -m "Added new feature"
   git push origin feature-name
   ```

3. **Create a Pull Request (PR) and tag relevant reviewers.**

## Contact & Support

For questions or contributions, please contact any of the project members. 🚀
