# database python file
# Copyright (c) 2019 Joan Chirinos

import uuid
from datetime import datetime

import sqlite3   # enable control of an sqlite database

DB_FILE = "data/main.db"

def create_db():
    '''
    Creates the database
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password TEXT, name TEXT, email TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS teams(team_id TEXT PRIMARY KEY, team_name TEXT, image_url TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS players(team_id TEXT, username TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS roles(team_id TEXT, username TEXT, role TEXT)")

    db.commit()
    db.close()

    return True;

#============USER Functions================

def get_users():
    '''
    Returns a list of all usernames
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('SELECT username FROM users')
    usernames = c.fetchall()

    print('USERNAMES:\n\t{}'.format(usernames))

    db.close()

    return usernames

def register(username, password, name, email):
    '''
    Attempts to register a user.
    Returns True, None on success; False, reason on failure
    Fails if username already in db
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    if username in get_users():
        return False, 'User already exists!'

    print('\n\nREGISTERING USER\n\n')
    print('\n\tusername: {}\n\tPassword: {}\n\tName: {}\n\tEmail: {}\n\n\n'.format(username, password, name, email))

    c.execute('INSERT INTO users VALUES(?, ?, ?, ?)', (username, password, name, email))

    db.commit()
    db.close()

    return True, None

def login(username, password):
    '''
    Checks if username matches password
    Returns True, None on success; False, reason on failure
    Fails if username not in db, or username doesn't match password
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('SELECT password FROM users WHERE username=?', (username,))

    check = c.fetchone()

    db.close()

    if check == None:
        return False, 'Incorrect username or password!'
    if check[0] != password:
        return False, 'Incorrect username or password!'
    return True, None

#============TEAM Functions================

def get_team_info(team_id):
    '''
    Gets team name and image url given team ID
    Returns True, (name, image_url) on succes
    Returns False, [] on failure
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    print(team_id)

    c.execute('SELECT team_name, image_url FROM teams WHERE team_id=?', (team_id,))
    out = c.fetchone()

    print(out)

    if out == None:
        return False, []
    return True, out

def create_team(username, team_name):
    '''
    Creates a new team given team name
    Adds username as team admin and player
    Returns True upon successful team creation
    Only ever breaks if uuid isn't unique.
    This should *never* happen, so I'll ignore this case
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    team_id = str(uuid.uuid4())

    c.execute('INSERT INTO teams VALUES(?, ?, ?)', (team_id, team_name, "https://i.ibb.co/D8JmVFX/ultimate.png"))
    c.execute('INSERT INTO players VALUES(?, ?)', (team_id, username))
    c.execute('INSERT INTO roles VALUES(?, ?, ?)', (team_id, username, 'admin'))
    c.execute('INSERT INTO roles VALUES(?, ?, ?)', (team_id, username, 'player'))

    db.commit()
    db.close()

    return True

def get_teams(username):
    '''
    Retrieves teams given username
    Returns True, [team_id...] if user is in any teams
    Returns False, [] otherwise
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('SELECT team_id FROM players WHERE username=?', (username,))

    teams = c.fetchall()
    print('teams: {}'.format(teams))

    if teams == []:
        return False, []
    return True, teams









if __name__ == '__main__':
     create_db()
