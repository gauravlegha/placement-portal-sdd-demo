# Placement Portal Application (MAD-I Project)

A role-based web application built with Flask and SQLite that facilitates campus recruitment activities between the Institute (Admin), Companies, and Students.

## Prerequisites
* Python 3.8 or higher installed on your system.

## Installation & Setup Instructions

1. **Extract the Project:**
   Unzip the project folder and open your terminal/command prompt inside the root directory of the project.

2. **Install Dependencies:**
   Install all required Python packages using the provided requirements file:
   `pip install -r requirements.txt`

3. **Initialize the Database:**
   The SQLite database (`placement.db`) is generated programmatically. Simply running the application for the first time will create the database, tables, and the default admin account automatically.

4. **Run the Application:**
   Start the Flask development server:
   `python app.py`

5. **Access the Portal:**
   Open your web browser and navigate to: **http://127.0.0.1:5000**

## Evaluator Login Credentials

To test the Admin functionalities, please use the pre-configured superuser account:
* **Role:** Admin
* **Username:** `admin`
* **Password:** `admin123`

*(Note: Companies and Students must self-register on the portal. Company accounts will require Admin approval from the dashboard before they can log in.)*

## Key Features to Test
* **File Uploads:** Register a student and test the PDF resume upload feature.
* **API Endpoints:** Navigate to `/api/drives`, `/api/students`, or `/api/applications` to view the JSON data endpoints.
* **Charts:** Check the Admin and Company dashboards for dynamic Chart.js data visualizations.