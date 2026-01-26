from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Workout(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    day = db.Column(db.String(50))          # Chest & Shoulders
    program_day = db.Column(db.String(20)) # Day 1 / Day 2

    exercise = db.Column(db.String(100))

    weight = db.Column(db.Integer)
    reps = db.Column(db.Integer)

    set_number = db.Column(db.Integer)

class DailyChecklist(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    date = db.Column(db.String(20))

    label = db.Column(db.String(100))  # Chest + Shoulders (Day 1)

    completed = db.Column(db.Boolean, default=True)
