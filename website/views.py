from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


# Defines the route for the home page, allowing GET and POST requests
@views.route('/', methods=['GET', 'POST'])
# Requires the user to be logged in to access the home page
@login_required
def home():
    """
    Handles the display and interaction of the home page.
    If the request method is POST and the note content is valid,
    adds the note to the database.
    """
    # Checks if the request method is POST
    if request.method == 'POST':
        # Gets the note content submitted from the HTML form
        note = request.form.get('note')

        # Checks if the note content is too short
        if len(note) < 1:
            # Displays an error message if the note content is too short
            flash('Note is too short!', category='error')
        else:
            # Creates a new note object, linking it to the current user
            new_note = Note(data=note, user_id=current_user.id)
            # Adds the new note to the database session
            db.session.add(new_note)
            # Commits the changes to the database
            db.session.commit()
            # Displays a success message after successfully adding the note
            flash('Note added!', category='success')

    # Renders and returns the home page template, passing in the current user's information
    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    # this function expects a JSON from the INDEX.js file
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    # 返回一个空的JSON对象
    return jsonify({})
