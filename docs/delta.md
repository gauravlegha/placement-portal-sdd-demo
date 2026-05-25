# Architecture Delta: Resume Analysis Feature

This document outlines the exact files that will be modified to implement the specification.

## 1. Environment Changes
* `requirements.txt`: 
  * Add `PyPDF2==3.0.1`

## 2. Backend Changes
* `app.py`:
  * Add `from PyPDF2 import PdfReader` to imports.
  * Modify `student_dashboard()` function.
  * Add file path resolution and PDF text extraction logic.
  * Add skill matching, scoring math, and suggestion logic.
  * Pass new variables to `student_dashboard.html`.
  * *Note: No database models will be altered. No migrations required.*

## 3. Frontend Changes
* `templates/student_dashboard.html`:
  * Insert a new Bootstrap-styled `<div>` below the student information block.
  * Add Jinja2 logic (`{% if ats_score is not none %}`) to render the ATS score, skill badges, and suggestions dynamically.