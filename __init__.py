# main python file
# Copyright (c) 2019 Joan Chirinos

import os

from flask import Flask, render_template, redirect, url_for, session, request, flash, get_flashed_messages
import datetime, uuid, re, json, random
from urllib.parse import parse_qs as pqs

from util import db

#============instantiate Flask object================
app = Flask(__name__)
app.secret_key = os.urandom(32)

#============Landing, login, register================

@app.route('/')
def landing():
    '''
    Landing page
    From here, the user can log in or register
    If user is already logged in, quickly redirects to team management page
    '''
    if 'username' in session:
        return redirect(url_for('team_management'))
    return render_template('landing.html')


@app.route('/login', methods=["POST"])
def login():
    '''
    Attempts to log the user in
    If user is already logged in, quickly redirects to team management page
    Upon succes, stores username in session and redirects user to team management page
    Upon failure, flashes a message and redirects user to landing page
    '''
    if 'username' in session:
        return redirect(url_for('team_management'))

    username = request.form['username']
    password = request.form['password']
    login_attempt = db.login(username, password)

    if login_attempt[0]:
        session['username'] = username
        return redirect(url_for('team_management'))
    else:
        flash(login_attempt[1], 'danger')
        return redirect(url_for('landing'))

@app.route('/register', methods=["POST"])
def register():
    '''
    Attempts to register user
    If user is already logged in, quickly redirects to team management page
    Upon success, flashes message and redirects user to landing page
    Upon failure, flashes message and redirects user to landing page
    '''
    if 'username' in session:
        return redirect(url_for('team_management'))

    username = request.form['username']
    password = request.form['password']
    name = request.form['name']
    email = request.form['email']

    register_attempt = db.register(username, password, name, email)

    if register_attempt[0]:
        flash('Account creation successful! You may now log in.', 'success')
    else:
        flash(register_attempt[1], 'danger')
    return redirect(url_for('landing'))

#============Team management================

@app.route('/teams')
def team_management():
    '''
    Team management page
    Shows user the teams they're in,
    and allows them to join a team with the team code
    '''
    if 'username' not in session:
        flash('You must be logged in to do that!', 'warning')
        return redirect(url_for('landing'))

    username = session['username']
    has_teams, teams = db.get_teams(username)

    print('teambois: ' + str(teams))

    teams = [db.get_team_info(id[0])[1] + (id[0],) for id in teams]
    team_chunks = [teams[i:i + 3] for i in range(0, len(teams), 3)]

    return render_template('team_management.html', has_teams=has_teams, team_chunks=team_chunks)


#============AJAX Functions================
@app.route('/new_team', methods=["POST"])
def create_team_ajax():
    username = session['username']
    team_name = request.form['teamName']

    db.create_team(username, team_name)
    return "All good here fellas"


#============run Flask App================













if __name__ == '__main__':
    app.debug = True
    app.run()
