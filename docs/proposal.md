# Feature Proposal: Resume Analysis & ATS Scoring

## 1. Objective
To enhance the Student Dashboard by adding an automated Resume Analysis feature. This will allow students to upload their resumes in PDF format and receive immediate, actionable feedback on their keyword optimization.

## 2. Motivation
Students often apply to placement drives without knowing if their resumes contain the industry-standard keywords that companies look for. By providing a basic Applicant Tracking System (ATS) score, we can guide students to improve their resumes before applying, increasing their chances of being shortlisted.

## 3. Proposed Feature
* **Upload Capability:** Students can upload a PDF version of their resume via the Edit Profile page.
* **Text Extraction:** The system will read the text from the uploaded PDF.
* **Keyword Matching:** The system will check the resume text against a predefined list of high-value technical skills (e.g., Python, SQL, Machine Learning, Flask).
* **Feedback Delivery:** The Student Dashboard will display:
    * An estimated ATS Score (out of 100).
    * A list of detected skills.
    * Actionable suggestions for missing core skills.

## 4. Out of Scope (What we are NOT building)
* **Deep Natural Language Processing (NLP):** We are not building a complex AI to understand context or grammar; we are doing simple keyword matching.
* **Database Storage:** To keep the system lightweight and avoid unnecessary database migrations, the ATS score and detected skills will be calculated dynamically on the fly when the dashboard loads, rather than being saved permanently in the database.