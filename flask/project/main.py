# main.py

import psycopg

from psycopg.rows import class_row
from flask import Blueprint, render_template
from flask_login import login_required, current_user

from .models import Target

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.id)

@main.route('/scan')
@login_required
def scan():
    return render_template('scan.html', name=current_user.id)

@main.route('/targets')
@login_required
def targets():
    with psycopg.connect("host=db user=postgres password=admin") as conn:
        with conn.cursor(row_factory=class_row(Target)) as cur:
            targets = cur.execute("SELECT * FROM targets WHERE owner = %s", (current_user.id,)).fetchall()
    return render_template('targets.html', targets=targets)
