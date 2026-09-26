from flask import Blueprint, session, redirect, render_template, request, url_for, flash
from app import db
from app.models import Task
tasks_bp = Blueprint('tasks' , __name__)

@tasks_bp.route("/")
def view_tasks():
    if 'user' not in session:
        return redirect(url_for("auth.login"))

    tasks = Task.query.filter_by(user_id=session["user_id"]).all()
    return render_template("tasks.html" , tasks=tasks)

@tasks_bp.route("/add", methods=["POST"])
def add_task():

    if "user" not in session:
        return redirect(url_for("auth.login"))

    title = request.form.get("title")

    if title:
        new_task = Task(
            title=title,
            status="Pending",
            user_id=session["user_id"]
        )

        db.session.add(new_task)
        db.session.commit()

        print("TASK ADDED:", new_task.id, new_task.title, new_task.user_id)

        flash("Task added successfully", "success")

    return redirect(url_for("tasks.view_tasks"))


@tasks_bp.route("/toggle/<int:task_id>" , methods=['POST'])
def toggle_status(task_id):
    task = Task.query.get(task_id)
    if task:
        if task.status == 'Pending':
            task.status = 'Working'
        elif task.status == 'Working':
            task.status = 'Done'

        else :
            task.status = 'Pending'

        db.session.commit()

        return redirect(url_for("tasks.view_tasks"))
            
@tasks_bp.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):

    if 'user' not in session:
        return redirect(url_for("auth.login"))

    task = Task.query.filter_by(
    id=task_id,
    user_id=session["user_id"]
).first()

    if task:
        db.session.delete(task)
        db.session.commit()

    return redirect(url_for("tasks.view_tasks"))



