from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# ================= USER =================

class User(db.Model):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(100), unique=True, nullable=False)

    password = db.Column(db.String(200), nullable=False)

    role = db.Column(db.String(20), nullable=False)


# ================= DISASTER =================

class Disaster(db.Model):

    __tablename__ = "disaster"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)

    disaster_type = db.Column(db.String(50))

    location = db.Column(db.String(100))

    description = db.Column(db.String(500))

    status = db.Column(
        db.String(20),
        default="Active"
    )


# ================= TASK =================

class Task(db.Model):

    __tablename__ = "task"

    id = db.Column(db.Integer, primary_key=True)

    disaster_id = db.Column(
        db.Integer,
        db.ForeignKey('disaster.id')
    )

    task_name = db.Column(db.String(100))

    description = db.Column(db.String(300))

    status = db.Column(
        db.String(20),
        default="Pending"
    )


# ================= VOLUNTEER ASSIGNMENT =================

class VolunteerAssignment(db.Model):

    __tablename__ = "volunteer_assignment"

    id = db.Column(db.Integer, primary_key=True)

    volunteer_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id')
    )

    task_id = db.Column(
        db.Integer,
        db.ForeignKey('task.id')
    )

    status = db.Column(
        db.String(20),
        default="Assigned"
    )


# ================= LOGS =================

class Log(db.Model):

    __tablename__ = "log"

    id = db.Column(db.Integer, primary_key=True)

    action = db.Column(db.String(200))

    created_at = db.Column(
        db.DateTime
    )