from app import app, db
from flask import render_template, redirect, url_for, flash, get_flashed_messages
from models import Task
from datetime import datetime
import forms

@app.route('/')
@app.route('/index')
def index():
    tasks = Task.query.all()
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = forms.AddTaskForm()
    if form.validate_on_submit(): 
        t = Task(title=form.title.data, date=datetime.utcnow())
        db.session.add(t)
        db.session.commit()
        flash('Task added to the database')
        return redirect(url_for('index'))
    return render_template('add.html', form=form)

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    task = Task.query.get(task_id)
    form = forms.AddTaskForm()
    if task:
        # populate fields with existing data
        if form.validate_on_submit():
            task.date = datetime.utcnow()  # update timestamp on each save
            task.title = form.title.data
            db.session.commit()
            flash("Task updated successfully")
            return redirect(url_for('index'))
        else:
            flash('Task not found')
        form.title.data = task.title
        return render_template('edit.html', form=form, task_id=task_id)
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['GET', 'POST'])
def delete(task_id):
    task = Task.query.get(task_id)
    form = forms.DeleteTaskForm()
    if task:
        # populate fields with existing data
        if form.validate_on_submit():
            db.session.delete(task)                
            db.session.commit()
            flash("Task has been deleted")
            return redirect(url_for('index'))        
        return render_template('delete.html', form=form, task_id=task_id, title=task.title)
    else:
        flash('Task not found')    
    return redirect(url_for('index'))