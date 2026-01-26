from flask import Flask, render_template, request, redirect
from models import db, Workout
from models import DailyChecklist
from datetime import datetime, date
import os 



app = Flask(__name__)

db_url = os.environ.get("DATABASE_URL")

# Force psycopg v3 driver instead of psycopg2
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+psycopg://", 1)

elif db_url and db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+psycopg://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/dashboard")
def dashboard():

    workouts = Workout.query.all()

    return render_template("dashboard.html", workouts=workouts)

@app.route("/chest-shoulders/day1")
def chest_shoulders_day1():

    workouts = Workout.query.filter_by(
        day="Chest & Shoulders",
        program_day="Day 1"
    ).all()

    return render_template(
        "muscle.html",
        workouts=workouts,
        title="Chest & Shoulders - Day 1"
    )


@app.route("/chest-shoulders/day2")
def chest_shoulders_day2():

    workouts = Workout.query.filter_by(
        day="Chest & Shoulders",
        program_day="Day 2"
    ).all()

    return render_template(
        "muscle.html",
        workouts=workouts,
        title="Chest & Shoulders - Day 2"
    )


@app.route("/back/day1")
def back_day1():

    workouts = Workout.query.filter_by(
        day="Back",
        program_day="Day 1"
    ).all()

    return render_template("muscle.html", workouts=workouts, title="Back - Day 1")


@app.route("/back/day2")
def back_day2():

    workouts = Workout.query.filter_by(
        day="Back",
        program_day="Day 2"
    ).all()

    return render_template("muscle.html", workouts=workouts, title="Back - Day 2")

@app.route("/arms/day1")
def arms_day1():

    workouts = Workout.query.filter_by(day="Arms", program_day="Day 1").all()

    return render_template("muscle.html", workouts=workouts, title="Arms - Day 1")


@app.route("/arms/day2")
def arms_day2():

    workouts = Workout.query.filter_by(day="Arms", program_day="Day 2").all()

    return render_template("muscle.html", workouts=workouts, title="Arms - Day 2")

@app.route("/legs/day1")
def legs_day1():

    workouts = Workout.query.filter_by(day="Legs", program_day="Day 1").all()

    return render_template("muscle.html", workouts=workouts, title="Legs - Day 1")


@app.route("/legs/day2")
def legs_day2():

    workouts = Workout.query.filter_by(day="Legs", program_day="Day 2").all()

    return render_template("muscle.html", workouts=workouts, title="Legs - Day 2")

@app.route("/add-workout")
def add_workout():
    selected_day = request.args.get("day")
    selected_exercise = request.args.get("exercise")

    return render_template(
        "add_workout.html",
        selected_day=selected_day,
        selected_exercise=selected_exercise
    )



@app.route("/save-workout", methods=["POST"])
def save_workout():

    new_workout = Workout(

    day=request.form["day"],
    program_day=request.form["program_day"],

    exercise=request.form["exercise"],

    weight=request.form["weight"],
    reps=request.form["reps"],

    set_number=request.form["set_number"]
)

    db.session.add(new_workout)
    db.session.commit()

    return redirect("/dashboard")
@app.route("/delete-workout/<int:id>")
def delete_workout(id):

    workout = Workout.query.get(id)

    db.session.delete(workout)
    db.session.commit()

    return redirect("/dashboard")
@app.route("/edit-workout/<int:id>")
def edit_workout(id):

    workout = Workout.query.get(id)

    return render_template("edit_workout.html", workout=workout)


@app.route("/update-workout/<int:id>", methods=["POST"])
def update_workout(id):

    workout = Workout.query.get(id)

    workout.day = request.form["day"]
    workout.exercise = request.form["exercise"]
    workout.weight = request.form["weight"]
    workout.reps = request.form["reps"]

    # Use set_number instead of sets
    workout.set_number = request.form["set_number"]

    db.session.commit()

    return redirect("/dashboard")
@app.route("/daily-checklist")
def daily_checklist():

    today = date.today().strftime("%d %b %Y")

    return render_template("daily_checklist.html", today=today)
@app.route("/mark-done/<label>")
def mark_done(label):

    today = date.today().strftime("%Y-%m-%d")

    # Check if entry for today already exists
    existing = DailyChecklist.query.filter_by(date=today).first()

    if existing:
        # Update instead of inserting
        existing.label = label
        existing.completed = True
    else:
        # Create new entry
        new_entry = DailyChecklist(
            date=today,
            label=label,
            completed=True
        )

        db.session.add(new_entry)

    db.session.commit()

    return redirect("/daily-checklist")
@app.route("/checklist-history")
def checklist_history():

    records = DailyChecklist.query.order_by(DailyChecklist.date).all()

    history = []
    streak = 0
    last_date = None

    for r in records:

        current_date = datetime.strptime(r.date, "%Y-%m-%d")

        # Streak logic
        if last_date and (current_date - last_date).days == 1:
            streak += 1
        else:
            streak = 1

        last_date = current_date

        # Convert weekday name
        day_name = current_date.strftime("%A")

        # Clean label text
        activity = r.label.replace("+", " ")

        history.append({
            "date": r.date,
            "day": day_name,
            "activity": activity,
            "streak": streak
        })

    # Show latest on top
    history.reverse()

    return render_template(
        "checklist_history.html",
        history=history
    )






# 1️⃣ 📱 Install to Home Screen (PWA like native app)