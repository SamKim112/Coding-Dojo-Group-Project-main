from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.user import User
from flask_app.models.event import Event


@app.route("/events/new")
def create_event():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('add_event.html')

@app.route('/events/new/process', methods=['POST'])
def process_event():
    if 'user_id' not in session:
        return redirect('/')
    
    if not Event.validate_event(request.form):
        return redirect('/events/new')

    data = {
        'users_id': session['user_id'],
        'event_name': request.form['event_name'],
        'location': request.form['location'],
        'participants': request.form['participants'],
        'date': request.form['date'],
        'messages': request.form['messages'],
    }
    Event.save(data)
    return redirect('/dashboard')

@app.route('/events/<int:id>')
def view_event(id):
    if 'user_id' not in session:
        return redirect('/')
    return render_template('event_view.html',event=Event.get_by_id({'id': id}))

@app.route('/events/edit/<int:id>')
def edit_event(id):
    if 'user_id' not in session:
        return redirect('/')

    return render_template('event_edit.html',event=Event.get_by_id({'id': id}))

@app.route('/events/edit/process/<int:id>', methods=['POST'])
def process_edit_event(id):
    if 'user_id' not in session:
        return redirect('/')
    if not Event.validate_event(request.form):
        return redirect(f'/events/edit/{id}') 

    data = {
        'id': id,
        'event_name': request.form['event_name'],
        'location': request.form['location'],
        'participants': request.form['participants'],
        'date': request.form['date'],
        'messages': request.form['messages'],
    }

    Event.update(data)
    return redirect('/dashboard')

@app.route('/events/destroy/<int:id>')
def destroy_event(id):
    if 'user_id' not in session:
        return redirect('/')

    Event.destroy({'id':id})
    return redirect('/dashboard')