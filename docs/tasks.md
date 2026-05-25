# Task Board: Resume Analysis Feature

## Phase 1: Setup & Dependencies
- [ ] **Task 1.1:** Add `PyPDF2` to `requirements.txt`.
- [ ] **Task 1.2:** Import `PdfReader` at the top of `app.py`.

## Phase 2: Backend Implementation (`app.py`)
- [ ] **Task 2.1:** Locate the `@app.route('/student_dashboard')` function.
- [ ] **Task 2.2:** Add a check to see if `student.resume` exists and the file is readable.
- [ ] **Task 2.3:** Implement PDF text extraction using `PyPDF2`.
- [ ] **Task 2.4:** Write the keyword matching logic against the predefined Data Science/Web Dev skills list.
- [ ] **Task 2.5:** Implement the scoring math (15 points per skill, max 100).
- [ ] **Task 2.6:** Generate the dynamic suggestions list based on missing skills.
- [ ] **Task 2.7:** Pass the new variables (`ats_score`, `found_skills`, `suggestions`) into the `render_template` return statement.

## Phase 3: Frontend Implementation (`templates/student_dashboard.html`)
- [ ] **Task 3.1:** Locate the HTML block containing the student's basic details.
- [ ] **Task 3.2:** Create a new Bootstrap-styled `<div>` for the "Live Resume Analysis" panel.
- [ ] **Task 3.3:** Add Jinja2 template logic (`{% if ats_score is not none %}`) to display the score and skills safely.
- [ ] **Task 3.4:** Add a loop to display the actionable suggestions.
- [ ] **Task 3.5:** Add the fallback message for users who haven't uploaded a resume yet.

## Phase 4: Verification
- [ ] **Task 4.1:** Log in as a student with a valid PDF and verify the score appears.
- [ ] **Task 4.2:** Log in as a student *without* a PDF and verify the fallback message appears instead of crashing.