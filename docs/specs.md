# Technical Specification: Resume Analysis & ATS Scoring

## 1. Overview
This feature calculates an Applicant Tracking System (ATS) score based on keyword matching. To maintain a lightweight architecture and avoid complex database migrations, the analysis will be performed dynamically ("on the fly") every time the student visits their dashboard.

## 2. Dependencies
* **Library:** `PyPDF2` (must be added to `requirements.txt`).
* **Purpose:** To extract raw text strings from the uploaded PDF file.

## 3. Backend Implementation (`app.py`)
**Target Route:** `@app.route('/student_dashboard')`

**Logic Flow:**
1. Retrieve the current user's `Student` record.
2. Check if a `resume` filename exists for the student.
3. If it exists, locate the file in `app.config['UPLOAD_FOLDER']`.
4. Use `PdfReader` to extract all text and convert it to lowercase.
5. **Keyword Matching Algorithm:**
   * Define a target list of Data Science and Web Dev skills: `['python', 'flask', 'sql', 'machine learning', 'data science', 'html', 'css', 'linux']`.
   * Iterate through the list and check if each skill exists in the extracted text.
6. **Scoring Engine:**
   * Each found skill is worth 15 points.
   * Maximum score is capped at 100.
7. **Suggestions Engine:**
   * If 'python' is missing, suggest adding it.
   * If total skills < 3, suggest adding more technical keywords.
8. Pass `ats_score`, `found_skills`, and `suggestions` to the template.

## 4. Frontend Implementation (`templates/student_dashboard.html`)
**UI Component:** A dedicated "Live Resume Analysis" panel.
**Placement:** Directly below the student's primary information and above the "Available Placement Drives" section.
**Display Elements:**
* ATS Score (e.g., 60 / 100).
* Found skills rendered as distinct visual tags/badges.
* A bulleted list of actionable suggestions (if any).
* If no resume is uploaded, display a prompt: "Please edit your profile to upload a PDF."

## 5. Edge Cases & Error Handling
* **File Not Found / Corrupt PDF:** If `PyPDF2` throws an exception reading the file, the backend will catch the error and pass `None` for the score, displaying an error message on the UI rather than crashing the application.