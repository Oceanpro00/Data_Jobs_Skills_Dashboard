# Data_Employment_Skills_Dashboard

## Repository Overview
This repository hosts the codebase for the **Data Career Skills Dashboard**, an interactive tool designed to help job seekers identify and prioritize the most in-demand skills for various career roles. Users will be able to:
- Input a **job title**.
- View a **ranked list of required skills**.
- Select skills they already have to dynamically adjust the ranking.
- Receive recommendations on **high-impact skills** to focus on for career growth.

This project is structured in **Sprint-based phases** following the roadmap outlined in the project plan.

## Project Team
- **Sean Schallberger**
- **Jose Traboulsi**
- **Karla Lopez**
- **Meghdut Noor**

## Datasets
We will source data from:
- **1.3M LinkedIn Jobs & Skills (2024)**  
- **Data Science Job Postings & Skills (2024)**

These datasets will be cleaned, standardized, and transformed for improved usability.

## Sprint Breakdown & Key Features

### Sprint 1: Data Collection & Cleaning
- **Data Ingestion & Initial Exploration**
  - Load dataset and evaluate job market representation.
  - Assess dataset completeness and coverage.
- **Data Integrity & Cleaning**
  - Standardize job titles and experience levels.
  - Remove duplicates and irrelevant job postings.
- **Ethical & Bias Evaluation**
  - Analyze biases in job postings (geographical skew, underrepresentation, etc.).
  - Document dataset limitations and ethical considerations.

### Sprint 2: Skill Processing
- **Extracting & Mapping Skills to Job Titles**
  - Structure and map skills to job titles and experience levels.
- **Ranking & Categorizing Skills**
  - Group skills into meaningful categories and rank them by demand.

### Sprint 3: Database & API Development
- **Uploading Processed Data to MongoDB**
  - Store cleaned and structured job skills data in a **MongoDB** database.
- **API Development for Skill Aggregation & Recommendations**
  - Develop Flask/FastAPI endpoints to serve job skills data dynamically.

### Sprint 4: Dashboard Development & Visualization
- **Develop Interactive Visualizations**
  - Build dashboards using **Plotly/D3.js**.
  - Create job market overview & personalized skill assessment views.
  - Implement **interactive charts, filters, and search options**.

## Technical Stack
| Component       | Technology |
|----------------|------------|
| **Backend & API** | Python, Flask, FastAPI (potentially) |
| **Database** | MongoDB (local or MongoDB Atlas) |
| **Visualization** | JavaScript (Plotly, D3.js) |
| **Hosting & Deployment** | Local deployment, optional cloud hosting |

## Project Milestones & Timeline
| Date | Task |
|------|------|
| **Week 1** | Project ideation, dataset selection, data cleaning |
| **Day 3-5** | MongoDB setup, Flask API development, initial visualizations |
| **Week 2** | Interactive dashboard development, final tweaks |
| **Final Days** | Presentation preparation & deployment |

## Deliverables
- **Final Interactive Dashboard**
- **MongoDB Database with Cleaned Data**
- **Flask API for Data Retrieval**
- **GitHub Repository (Code, Data, README)**
- **Presentation Deck (10-minute demo)**

## Contribution Guidelines
1. **Fork the repository & create a feature branch**
   ```sh
   git checkout -b feature-name
   ```
2. **Commit and push your changes**
   ```sh
   git commit -m "Added new feature"
   git push origin feature-name
   ```
3. **Create a Pull Request (PR)**

## License
This project is licensed under the **MIT License**.

## Contact
For any questions or contributions, please contact any of the project members.
