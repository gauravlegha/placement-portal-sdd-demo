
from flask import Flask, render_template, redirect, url_for, request, flash, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
import os
from werkzeug.utils import secure_filename
from datetime import datetime
app = Flask(__name__)

#configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placement.db'
app.config['SECRET_KEY'] = 'secret_key_123' # Required for security later
app.config['UPLOAD_FOLDER'] = 'static/resumes'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
# DATABASE MODELS 

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, default=True) # 'admin', 'company', or 'student'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(100), nullable=False) 
    hr_contact = db.Column(db.String(100)) # <-- ADD THIS
    website = db.Column(db.String(100)) 
    is_approved = db.Column(db.Boolean, default=False)
    is_blacklisted = db.Column(db.Boolean, default=False)
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    full_name = db.Column(db.String(100), nullable=False) 
    education = db.Column(db.String(200)) 
    skills = db.Column(db.String(200))
    resume = db.Column(db.String(200)) 

class Drive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id')) 
    job_title = db.Column(db.String(100), nullable=False) 
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='Pending') 

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id')) 
    drive_id = db.Column(db.Integer, db.ForeignKey('drive.id'))
    status = db.Column(db.String(20), default='Applied') 
    __table_args__ = (
        db.UniqueConstraint('student_id', 'drive_id', name='_student_drive_uc'),
    )
# Homepage Route
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        if len(password) < 6:
            flash('Validation Error: Password must be at least 6 characters long.', 'danger')
            return redirect(url_for('register'))
            
        if role not in ['student', 'company']:
            flash('Validation Error: Invalid role selected.', 'danger')
            return redirect(url_for('register'))
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        if role == 'student':
            new_student = Student(user_id=new_user.id, full_name=username)
            
            resume_file = request.files.get('resume')
            if resume_file and resume_file.filename != '':
                filename = secure_filename(resume_file.filename)
                save_name = f"{username}_{filename}"
                resume_file.save(os.path.join(app.config['UPLOAD_FOLDER'], save_name))
                new_student.resume = save_name

            db.session.add(new_student)
            
        elif role == 'company':
            new_company = Company(user_id=new_user.id, name=username)
            db.session.add(new_company)
        
        db.session.commit()
        flash('Registration successful! You can now log in.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):    
            if user.role == 'company':
                company_record = Company.query.filter_by(user_id=user.id).first()
                if not company_record.is_approved:
                    flash('Your account is pending Admin approval. Please try again later.')
                    return redirect(url_for('login'))

            login_user(user) 
            
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.role == 'company':
                return redirect(url_for('company_dashboard'))
            elif user.role == 'student':
                return redirect(url_for('student_dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password.')
        
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))



@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Access denied. Admins only.')
        return redirect(url_for('home'))

    total_students = Student.query.count()
    total_companies = Company.query.count()
    total_drives = Drive.query.count()
    total_apps = Application.query.count()
    total_placements = Application.query.filter_by(status='Selected').count()

    pending_companies = Company.query.filter_by(is_approved=False).all()
    pending_drives = Drive.query.filter_by(status='Pending').all()

    all_drives = Drive.query.all()
    
    student_search = request.args.get('student_search', '')
    company_search = request.args.get('company_search', '')

    if student_search:
        students = Student.query.filter(Student.full_name.ilike(f"%{student_search}%")).all()
    else:
        students = Student.query.all()

    if company_search:
        companies = Company.query.filter(Company.name.ilike(f"%{company_search}%")).all()
    else:
        companies = Company.query.all()

    return render_template('admin_dashboard.html', 
                           student_count=total_students, 
                           company_count=total_companies,
                           drive_count=total_drives,
                           app_count=total_apps,
                           pending_companies=pending_companies,
                           pending_drives=pending_drives,
                           students=students,
                           companies=companies,
                           student_search=student_search,
                           company_search=company_search,
                           all_drives=all_drives,
                           placements_count=total_placements)


@app.route('/company_dashboard')
@login_required
def company_dashboard():
    if current_user.role != 'company':
        flash('Access denied. Companies only.')
        return redirect(url_for('home'))

    company = Company.query.filter_by(user_id=current_user.id).first()
    drives = Drive.query.filter_by(company_id=company.id).all()
    job_titles = []
    app_counts = []
        
    for drive in drives:
        job_titles.append(drive.job_title)
        count = Application.query.filter_by(drive_id=drive.id).count()
        app_counts.append(count)

    return render_template('company_dashboard.html', company=company, drives=drives,
                           job_titles=job_titles, 
                           app_counts=app_counts)

@app.route('/create_drive', methods=['GET', 'POST'])
@login_required
def create_drive():
    if current_user.role != 'company':
        flash('Access denied. Companies only.')
        return redirect(url_for('home'))

    company = Company.query.filter_by(user_id=current_user.id).first()

    if request.method == 'POST':
        job_title = request.form.get('job_title')
        description = request.form.get('description')

        new_drive = Drive(company_id=company.id, job_title=job_title, description=description)
        db.session.add(new_drive)
        db.session.commit()

        flash('Placement Drive created! It is pending Admin approval.')
        return redirect(url_for('company_dashboard'))

    return render_template('create_drive.html')



@app.route('/student_dashboard')
@login_required
def student_dashboard():
    if current_user.role != 'student':
        flash('Access denied. Students only.')
        return redirect(url_for('home'))

    student = Student.query.filter_by(user_id=current_user.id).first()

    search_query = request.args.get('search', '') # Get what they typed in the search bar

    if search_query:
        # Create a search term with wildcards (%) for partial matches
        search_term = f"%{search_query}%"
        # Join Drive and Company tables to search across job title, description, AND company name
        available_drives = Drive.query.join(Company).filter(
            Drive.status == 'Approved',
            (Drive.job_title.ilike(search_term)) | 
            (Drive.description.ilike(search_term)) |
            (Company.name.ilike(search_term))
        ).all()
    else:
        available_drives = Drive.query.filter_by(status='Approved').all()

    my_applications = Application.query.filter_by(student_id=student.id).all()

    status_counts = {
        'Applied': 0,
        'Shortlisted': 0,
        'Selected': 0,
        'Rejected': 0
    }
    for app in my_applications:
        if app.status in status_counts:
            status_counts[app.status] += 1
        else:
            status_counts[app.status] = 1
    
    applied_drive_ids = [app.drive_id for app in my_applications]

    return render_template('student_dashboard.html', 
                           student=student, 
                           available_drives=available_drives,
                           my_applications=my_applications,
                           applied_drive_ids=applied_drive_ids,
                           search_query=search_query,
                           status_counts=status_counts) 


@app.route('/approve_company/<int:company_id>', methods=['POST'])
@login_required
def approve_company(company_id):
    # Security check again
    if current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('home'))

    # Find the company and change status
    company = Company.query.get_or_404(company_id)
    company.is_approved = True
    db.session.commit()
    
    flash(f'Company {company.name} has been approved!')
    return redirect(url_for('admin_dashboard'))

@app.route('/approve_drive/<int:drive_id>', methods=['POST'])
@login_required
def approve_drive(drive_id):
    if current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('home'))

    drive = Drive.query.get_or_404(drive_id)
    drive.status = 'Approved'
    db.session.commit()
    
    flash(f'Placement Drive "{drive.job_title}" has been approved!')
    return redirect(url_for('admin_dashboard'))

@app.route('/apply/<int:drive_id>', methods=['POST'])
@login_required
def apply_to_drive(drive_id):
    if current_user.role != 'student':
        flash('Access denied.')
        return redirect(url_for('home'))
    
    student = Student.query.filter_by(user_id=current_user.id).first()
    
    # Double-check they haven't applied already to prevent duplicates
    existing_app = Application.query.filter_by(student_id=student.id, drive_id=drive_id).first()
    
    if not existing_app:
        # Create the new application record
        new_app = Application(student_id=student.id, drive_id=drive_id)
        db.session.add(new_app)
        db.session.commit()
        flash('Successfully applied to the placement drive!')
    else:
        flash('You have already applied to this drive.')
        
    return redirect(url_for('student_dashboard'))

@app.route('/view_applications/<int:drive_id>')
@login_required
def view_applications(drive_id):
    if current_user.role not in ['company', 'admin']:
        flash('Access denied.')
        return redirect(url_for('home'))

    drive = Drive.query.get_or_404(drive_id)
    
    if current_user.role == 'company':
        company = Company.query.filter_by(user_id=current_user.id).first()
        if drive.company_id != company.id:
            flash('You can only view applications for your own drives.')
            return redirect(url_for('company_dashboard'))

    applications = Application.query.filter_by(drive_id=drive.id).all()
    
    app_details = []
    for app in applications:
        student = Student.query.get(app.student_id)
        app_details.append({
            'app_id': app.id,
            'student_name': student.full_name,
            'education': student.education, 
            'skills': student.skills,       
            'resume': student.resume,       
            'status': app.status
        })

    return render_template('view_applications.html', drive=drive, app_details=app_details)

@app.route('/update_application/<int:app_id>', methods=['POST'])
@login_required
def update_application(app_id):
    if current_user.role != 'company':
        flash('Access denied.')
        return redirect(url_for('home'))

    application = Application.query.get_or_404(app_id)
    new_status = request.form.get('new_status')
    
    if new_status in ['Applied', 'Shortlisted', 'Selected', 'Rejected']:
        application.status = new_status
        db.session.commit()
        flash(f'Application status updated to {new_status}!')
        
    return redirect(url_for('view_applications', drive_id=application.drive_id))

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if current_user.role != 'student':
        flash('Access denied. Students only.')
        return redirect(url_for('home'))

    student = Student.query.filter_by(user_id=current_user.id).first()

    if request.method == 'POST':
        student.full_name = request.form.get('full_name')
        student.education = request.form.get('education')
        student.skills = request.form.get('skills')
        
        # Handle a new resume upload if they chose one
        resume_file = request.files.get('resume')
        if resume_file and resume_file.filename != '':
            filename = secure_filename(resume_file.filename)
            save_name = f"{current_user.username}_{filename}"
            resume_file.save(os.path.join(app.config['UPLOAD_FOLDER'], save_name))
            student.resume = save_name # Update the database with the new filename
            
        db.session.commit()
        flash('Profile updated successfully!')
        return redirect(url_for('student_dashboard'))

    return render_template('edit_profile.html', student=student)

@app.route('/static/resumes/<filename>')
def download_resume(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        flash('Access denied. Admins only.')
        return redirect(url_for('home'))

    user_to_delete = User.query.get_or_404(user_id)
    
    if user_to_delete.role == 'admin':
        flash('Cannot delete the master admin account!')
        return redirect(url_for('admin_dashboard'))

    if user_to_delete.role == 'student':
        student = Student.query.filter_by(user_id=user_to_delete.id).first()
        if student:
            Application.query.filter_by(student_id=student.id).delete()
            db.session.delete(student)
            
    elif user_to_delete.role == 'company':
        company = Company.query.filter_by(user_id=user_to_delete.id).first()
        if company:
            drives = Drive.query.filter_by(company_id=company.id).all()
            for drive in drives:
                Application.query.filter_by(drive_id=drive.id).delete()
                db.session.delete(drive)
            db.session.delete(company)

    db.session.delete(user_to_delete)
    db.session.commit()
    
    flash(f'Account for {user_to_delete.username} has been successfully deleted.')
    return redirect(url_for('admin_dashboard'))

@app.route('/close_drive/<int:drive_id>', methods=['POST'])
@login_required
def close_drive(drive_id):
    if current_user.role != 'company':
        flash('Access denied. Companies only.')
        return redirect(url_for('home'))

    drive = Drive.query.get_or_404(drive_id)
    company = Company.query.filter_by(user_id=current_user.id).first()
    
    if drive.company_id != company.id:
        flash('You can only close your own placement drives.')
        return redirect(url_for('company_dashboard'))

    drive.status = 'Closed'
    db.session.commit()
    
    flash(f'Placement Drive "{drive.job_title}" has been closed. Students can no longer apply.')
    return redirect(url_for('company_dashboard'))

# API ENDPOINTS

@app.route('/api/drives', methods=['GET'])
def api_get_drives():
    drives = Drive.query.filter_by(status='Approved').all()
    
    drives_list = []
    for drive in drives:
        company = Company.query.get(drive.company_id)
        
        drives_list.append({
            'drive_id': drive.id,
            'company_name': company.name if company else 'Unknown',
            'job_title': drive.job_title,
            'description': drive.description,
            'status': drive.status
        })
        
    return jsonify({
        'success': True,
        'count': len(drives_list),
        'drives': drives_list
    })

@app.route('/api/students', methods=['GET'])
def api_get_students():
    students = Student.query.all()
    
    student_list = []
    for s in students:
        student_list.append({
            'student_id': s.id,
            'name': s.full_name,
            'education': s.education or 'Not provided',
            'skills': s.skills or 'Not provided'
        })
        
    return jsonify({
        'success': True,
        'count': len(student_list),
        'students': student_list
    })


@app.route('/reject_drive/<int:drive_id>', methods=['POST'])
@login_required
def reject_drive(drive_id):
    if current_user.role != 'admin':
        flash('Access denied. Admins only.')
        return redirect(url_for('home'))

    drive = Drive.query.get_or_404(drive_id)
    
    # Update the status to Rejected
    drive.status = 'Rejected'
    db.session.commit()
    
    flash(f'Placement Drive "{drive.job_title}" has been rejected.')
    return redirect(url_for('admin_dashboard'))

@app.route('/api/applications', methods=['GET'])
def api_get_applications():
    applications = Application.query.all()
    
    app_list = []
    for app in applications:
        app_list.append({
            'application_id': app.id,
            'student_id': app.student_id,
            'drive_id': app.drive_id,
            'status': app.status
        })
        
    return jsonify({
        'success': True,
        'count': len(app_list),
        'applications': app_list
    })

if __name__ == '__main__':
    app.run(debug=True)


