from app import app, db
from flask import flash, redirect, url_for, request, session, make_response
import json
import httplib2

# Google Sign-out flow
@app.route('/gdisconnect')
def gdisconnect():
    # Step 1: Check if user is present in session.
    access_token = session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps(
                   'Current user not connected.'),
                   401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is {}'.format(access_token)
    print 'User name is: '
    print session['username']
    # Step 2: API call to revoke the access token stored in session.
    url = 'https://accounts.google.com/o/oauth2/revoke?token={}'.format(session['access_token'])  # NOQA
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    # Step 3: 200 or 400 status both mean the user should be logged out and
    # deleted from session.
    if result['status'] == '200':
        del session['access_token']
        del session['gplus_id']
        del session['username']
        del session['email']
        del session['picture']
        del session['user_id']
        response = 'Logged out.'
        flash(response)
        return redirect(url_for('index'))
    elif result['status'] == '400':
        del session['access_token']
        del session['gplus_id']
        del session['username']
        del session['email']
        del session['picture']
        del session['user_id']
        response = 'Logged out.'
        flash(response)
        return redirect(url_for('index'))
    else:
        response = 'Failed to revoke token for given user.'
        flash(response)
        return redirect(url_for('index'))
