from app import app, db
from flask import flash, redirect, url_for, request, make_response, session
from app.models.user import User
import json
import httplib2
import requests
from oauth2client import client


# Handles Google Sign-in flow server-side
@app.route('/gconnect', methods=['POST'])
def gConnect():
    # Step 1: Validate state token.
    if request.args.get('state') != session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Step 2: Obtain authorization code from Google JSON response
    code = request.data
    # Step 3: Exchange auth code for credentials object.
    credentials = client.credentials_from_clientsecrets_and_code(
                  app.config['CLIENT_SECRET_FILE'],
                  ['profile', 'email'],
                  code)

    # Step 4: API Call to check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Step 5: match access token to current user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Step 6: match access token to app's client ID.
    if result['issued_to'] != app.config['CLIENT_ID']:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response
    # Step 7: Store access token in session for disconnect
    session['access_token'] = credentials.access_token
    session['gplus_id'] = gplus_id

    # Step 8: API call for user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    # Step 9: store user info in session
    session['provider'] = 'google'
    session['username'] = data['name']
    session['picture'] = data['picture']
    session['email'] = data['email']
    # Step 10: Determine if user exists in database, otherwise create it.
    user_id = getUserID(session['email'])
    if not user_id:
        user_id = createUser(session)
    session['user_id'] = user_id
    return redirect(url_for('index'))


# Helper functions for storing users in database.
def createUser(login_session):
    newUser = User(username=session['username'],
                   email=session['email'],
                   picture=session['picture'],
                   password_hash="notused")
    db.session.add(newUser)
    db.session.commit()
    user = db.session.query(User).filter_by(email=session['email']).one()
    return user.id


def getUserID(email):
    try:
        user = db.session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None
