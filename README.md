# Spec-Driven Development vs. Vibe Coding 

**Author:** Gaurav 
**Program:** BS in Data Science, IIT Madras
**Base Project:** Placement Portal Application (Flask/SQLite)
**New Feature:** Automated Resume Analysis & ATS Scoring

---

## 🎯 Assignment Overview
This repository demonstrates the contrast between **Vibe Coding** and **Spec-Driven Development (SDD)** methodologies. 

The identical feature (Resume Analysis) was implemented across two separate branches. The feature extracts text from student uploaded PDFs and calculates a keyword-based ATS score optimized for Data Science and Web Development roles.

### How to Evaluate This Repository

Please review the two branches to observe the contrast in methodologies:

#### 1. Branch: `vibe_coded_submission`
* **Methodology:** The feature was built rapidly without formal planning, documentation, or architecture design. 
* **Key Characteristics:** * Inline styling in HTML templates.
  * Logic tightly coupled within existing routes.
  * Zero preliminary documentation.
  * Focus was entirely on immediate execution and working code.

#### 2. Branch: `sdd_submission` (Current)
* **Methodology:** The feature was built strictly following the Spec-Driven Development philosophy. The documentation acted as the single Source of Truth before any code was written.
* **Key Characteristics:**
  * **The `docs/` Directory:** Please review this folder first. It contains the complete paper trail:
    * `proposal.md` (What and Why)
    * `spec.md` (The technical blueprint and Source of Truth)
    * `tasks.md` (Implementation breakdown)
    * `project.md` & `delta.md` (Architecture context)
  * **Code Implementation:** The code in `app.py` and `student_dashboard.html` was written strictly to fulfill the requirements outlined in `spec.md`, demonstrating planned error handling and structured integration.

---

## ⚙️ Local Setup Instructions

If you wish to run the code locally to test the feature:

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
Initialize Database (If needed):

Bash
python upgrade_db.py
Run the Application:

Bash
python app.py
Access the Portal:
Navigate to http://127.0.0.1:5000.

To test the feature: Log in or register as a Student, click "Edit Profile," upload a sample PDF resume, and view the dashboard.


