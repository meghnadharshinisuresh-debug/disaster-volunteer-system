from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretkey'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


# =====================================================
# USER TABLE
# =====================================================

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False
    )


# =====================================================
# HELP REQUEST TABLE
# =====================================================

class HelpRequest(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100)
    )

    phone = db.Column(
        db.String(20)
    )

    location = db.Column(
        db.String(100)
    )

    disaster_type = db.Column(
        db.String(50)
    )

    priority = db.Column(
        db.String(20)
    )

    people_affected = db.Column(
        db.Integer
    )

    description = db.Column(
        db.String(500)
    )

    status = db.Column(
        db.String(20),
        default="Pending"
    )
    # ---------------- EMERGENCY REPORT TABLE ----------------
class EmergencyReport(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100)
    )

    phone = db.Column(
        db.String(20)
    )

    emergency_type = db.Column(
        db.String(100)
    )

    latitude = db.Column(
        db.String(50)
    )

    longitude = db.Column(
        db.String(50)
    )

    status = db.Column(
        db.String(50),
        default="Pending"
    )

    assigned_to = db.Column(
        db.String(100)
    )

# =====================================================
# DISASTER TABLE
# =====================================================

class Disaster(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(100)
    )

    disaster_type = db.Column(
        db.String(50)
    )

    location = db.Column(
        db.String(100)
    )

    description = db.Column(
        db.String(500)
    )

    status = db.Column(
        db.String(20),
        default="Active"
    )


# =====================================================
# TASK TABLE
# =====================================================

class Task(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    disaster_id = db.Column(
        db.Integer,
        db.ForeignKey('disaster.id')
    )

    task_name = db.Column(
        db.String(100)
    )

    description = db.Column(
        db.String(500)
    )

    status = db.Column(
        db.String(20),
        default="Pending"
    )


# =====================================================
# VOLUNTEER ASSIGNMENT TABLE
# =====================================================

class VolunteerAssignment(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    volunteer_name = db.Column(
        db.String(100)
    )

    task_id = db.Column(
        db.Integer,
        db.ForeignKey('task.id')
    )

    status = db.Column(
        db.String(20),
        default="Assigned"
    )


# =====================================================
# HOME
# =====================================================

@app.route('/')
def home():
    return render_template('index.html')


# =====================================================
# REGISTER
# =====================================================

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']

        email = request.form['email']

        password = request.form['password']

        role = request.form['role']

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            return "Email already registered"

        hashed_password = bcrypt.generate_password_hash(
            password
        ).decode('utf-8')

        user = User(

            name=name,

            email=email,

            password=hashed_password,

            role=role

        )

        db.session.add(user)

        db.session.commit()

        return redirect('/login')

    return render_template('register.html')


# =====================================================
# LOGIN
# =====================================================

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']

        password = request.form['password']

        user = User.query.filter_by(
            email=email
        ).first()

        if user and bcrypt.check_password_hash(
            user.password,
            password
        ):

            session['user'] = user.name
            session['user_id'] = user.id
            session['role'] = user.role

            return redirect('/dashboard')

        return "Invalid Email or Password"

    return render_template('login.html')
# =====================================================
# DASHBOARD
# =====================================================

@app.route('/dashboard')
def dashboard():

    if 'user' not in session:
        return redirect('/login')

    total_users = User.query.count()

    total_requests = HelpRequest.query.count()

    total_sos = EmergencyReport.query.count()

    pending_sos = EmergencyReport.query.filter_by(
        status="Pending"
    ).count()

    resolved_sos = EmergencyReport.query.filter_by(
        status="Resolved"
    ).count()

    active_disasters = Disaster.query.count()

    pending_tasks = Task.query.filter_by(
        status="Pending"
    ).count()

    completed_tasks = Task.query.filter_by(
        status="Completed"
    ).count()

    return render_template(

        'dashboard.html',

        user=session['user'],

        role=session['role'],

        total_users=total_users,

        total_requests=total_requests,

        total_sos=total_sos,

        pending_sos=pending_sos,

        resolved_sos=resolved_sos,

        active_disasters=active_disasters,

        pending_tasks=pending_tasks,

        completed_tasks=completed_tasks

    )
# =====================================================
# CREATE HELP REQUEST
# =====================================================

@app.route('/help_request', methods=['GET', 'POST'])
def help_request():

    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':

        help_data = HelpRequest(

            name=request.form['name'],

            phone=request.form['phone'],

            location=request.form['location'],

            disaster_type=request.form['disaster_type'],

            priority=request.form['priority'],

            people_affected=request.form['people_affected'],

            description=request.form['description']

        )

        db.session.add(help_data)

        db.session.commit()

        return redirect('/dashboard')

    return render_template('help_request.html')


# =====================================================
# ALL HELP REQUESTS
# =====================================================

@app.route('/all_requests')
def all_requests():

    if 'user' not in session:
        return redirect('/login')

    requests = HelpRequest.query.all()

    return render_template(

        'all_requests.html',

        requests=requests,

        role=session['role']

    )

# =====================================================
# COMPLETE REQUEST
# =====================================================

@app.route('/complete_request/<int:id>')
def complete_request(id):

    if 'user' not in session:
        return redirect('/login')

    req = HelpRequest.query.get_or_404(id)

    req.status = "Completed"

    db.session.commit()

    return redirect('/all_requests')


# =====================================================
# DELETE REQUEST
# =====================================================

@app.route('/delete_request/<int:id>')
def delete_request(id):

    if 'user' not in session:
        return redirect('/login')

    req = HelpRequest.query.get_or_404(id)

    db.session.delete(req)

    db.session.commit()

    return redirect('/all_requests')


# =====================================================
# USERS PAGE
# =====================================================

@app.route('/users')
def users():

    if 'user' not in session:
        return redirect('/login')

    if session['role'] != 'Admin':
        return "Access Denied"

    all_users = User.query.all()

    return render_template(

        'users.html',

        users=all_users

    )


# =====================================================
# DELETE USER
# =====================================================

@app.route('/delete_user/<int:id>')
def delete_user(id):

    if 'user' not in session:
        return redirect('/login')

    if session['role'] != 'Admin':
        return "Access Denied"

    user = User.query.get_or_404(id)

    db.session.delete(user)

    db.session.commit()

    return redirect('/users')


# =====================================================
# CREATE DISASTER
# =====================================================

@app.route('/create_disaster', methods=['GET', 'POST'])
def create_disaster():

    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':

        disaster = Disaster(

            title=request.form['title'],

            disaster_type=request.form['disaster_type'],

            location=request.form['location'],

            description=request.form['description']

        )

        db.session.add(disaster)

        db.session.commit()

        return redirect('/disasters')

    return render_template('create_disaster.html')


# =====================================================
# VIEW DISASTERS
# =====================================================

@app.route('/disasters')
def disasters():

    if 'user' not in session:
        return redirect('/login')

    all_disasters = Disaster.query.all()

    return render_template(

        'disasters.html',

        disasters=all_disasters

    )


# =====================================================
# DELETE DISASTER
# =====================================================

@app.route('/delete_disaster/<int:id>')
def delete_disaster(id):

    if 'user' not in session:
        return redirect('/login')

    disaster = Disaster.query.get_or_404(id)

    db.session.delete(disaster)

    db.session.commit()

    return redirect('/disasters')
# =====================================================
# CREATE TASK
# =====================================================

@app.route('/create_task', methods=['GET', 'POST'])
def create_task():

    if 'user' not in session:
        return redirect('/login')

    disasters = Disaster.query.all()

    if request.method == 'POST':

        task = Task(

            disaster_id=request.form['disaster_id'],

            task_name=request.form['task_name'],

            description=request.form['description']

        )

        db.session.add(task)

        db.session.commit()

        return redirect('/tasks')

    return render_template(
        'create_task.html',
        disasters=disasters
    )


# =====================================================
# VIEW TASKS
# =====================================================

@app.route('/tasks')
def tasks():

    if 'user' not in session:
        return redirect('/login')

    all_tasks = Task.query.all()

    return render_template(
        'tasks.html',
        tasks=all_tasks
    )


# =====================================================
# ASSIGN VOLUNTEER
# =====================================================

@app.route('/assign_volunteer/<int:id>', methods=['GET', 'POST'])
def assign_volunteer(id):

    if 'user' not in session:
        return redirect('/login')

    task = Task.query.get_or_404(id)

    volunteers = User.query.filter_by(
        role='Volunteer'
    ).all()

    if request.method == 'POST':

        assignment = VolunteerAssignment(

            volunteer_name=request.form['volunteer_name'],

            task_id=id,

            status='Assigned'

        )

        task.status = "Assigned"

        db.session.add(assignment)

        db.session.commit()

        return redirect('/tasks')

    return render_template(
        'assign_volunteer.html',
        task=task,
        volunteers=volunteers
    )


# =====================================================
# UPDATE TASK STATUS
# =====================================================

@app.route('/update_task/<int:id>/<status>')
def update_task(id, status):

    if 'user' not in session:
        return redirect('/login')

    task = Task.query.get_or_404(id)

    task.status = status

    db.session.commit()

    return redirect('/tasks')


# =====================================================
# DELETE TASK
# =====================================================

@app.route('/delete_task/<int:id>')
def delete_task(id):

    if 'user' not in session:
        return redirect('/login')

    task = Task.query.get_or_404(id)

    db.session.delete(task)

    db.session.commit()

    return redirect('/tasks')



# ---------------- SOS PAGE ----------------

@app.route('/sos', methods=['GET', 'POST'])
def sos():

    if request.method == 'POST':

        print("LAT =", request.form['latitude'])
        print("LON =", request.form['longitude'])

        report = EmergencyReport(

            name=request.form['name'],
            phone=request.form['phone'],
            emergency_type=request.form['emergency_type'],
            latitude=request.form['latitude'],
            longitude=request.form['longitude']

        )

        db.session.add(report)
        db.session.commit()

        return redirect('/view_sos')

    return render_template('sos.html')


# ---------------- VIEW SOS ----------------

@app.route('/view_sos')
def view_sos():

    reports = EmergencyReport.query.all()

    return render_template(
        'view_sos.html',
        reports=reports
    )
@app.route('/assign_sos/<int:id>')
def assign_sos(id):

    report = EmergencyReport.query.get(id)

    report.assigned_to = session['user']

    report.status = "In Progress"

    db.session.commit()

    return redirect('/view_sos')


@app.route('/resolve_sos/<int:id>')
def resolve_sos(id):

    report = EmergencyReport.query.get(id)

    report.status = "Resolved"

    db.session.commit()

    return redirect('/view_sos')
# =====================================================
# LOGOUT
# =====================================================

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')

with app.app_context():
    db.create_all()
# =====================================================
# CREATE DATABASE
# =====================================================

if __name__ == "__main__":

    with app.app_context():

        db.create_all()

    app.run(debug=True)