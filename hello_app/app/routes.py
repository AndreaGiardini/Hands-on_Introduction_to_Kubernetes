import os
import socket
import time

from app import app
from flask import render_template, redirect, url_for, request


# Application State
isAlive = True
isReady = True

@app.route('/')
@app.route('/index')
def index():
    return render_template(
            'hello.html',
            name=socket.gethostname(),
            env_color=os.getenv('COLOR') if os.getenv('COLOR') else 'black'
            )

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = None
    if request.method == 'POST':
        admin_user = None
        admin_pass = None
        # If LOGIN_USER and LOGIN_PASS are defined use them for login
        if os.getenv('LOGIN_USER') and os.getenv('LOGIN_PASS'):
            admin_user = os.getenv('LOGIN_USER')
            admin_pass = os.getenv('LOGIN_PASS')
        # If a secret file is mounted in /auth/cred.txt with username:pass
        # use the credentials as login
        if os.path.isfile('/auth/cred.txt'):
            file = open('/auth/cred.txt', 'r')
            admin_user, admin_pass = file.read().rstrip().split(':')
            file.close()
        if request.form['username'] != admin_user or request.form['password'] != admin_pass:
            msg = 'Authentication Failed'
        else:
            msg = 'Authentication Successful'
    return render_template('login.html', msg=msg)

@app.route('/liveness')
def liveness():
    return "Alive" if isAlive else ("Not Alive", 500)

@app.route('/liveness/change')
def livenessChange():
    global isAlive
    isAlive = not isAlive
    return "Status changed"

@app.route('/prime/')
@app.route('/prime/<upperLimit>')
def prime(upperLimit=5000):
    # Initialize a list
    startTime = time.time()
    primes = []
    for possiblePrime in range(2, int(upperLimit) + 1):
        # Assume number is prime until shown it is not.
        isPrime = True
        for num in range(2, possiblePrime):
            if possiblePrime % num == 0:
                isPrime = False
                break
        if isPrime:
            primes.append(possiblePrime)
    #return(' '.join(str(e) for e in primes))
    return "The calculation took: " + str(time.time() - startTime) + " seconds"

@app.route('/readiness')
def readiness():
    return "Ready" if isReady else ("Not Ready", 500)

@app.route('/readiness/change')
def readinessChange():
    global isReady
    isReady = not isReady
    return "Status changed"
