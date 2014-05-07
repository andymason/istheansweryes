from flask import Flask
from flask import render_template
from flask import request
from google.appengine.ext import ndb
from os import urandom
import base64

app = Flask(__name__)

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

class Question(ndb.Model):
    text = ndb.StringProperty()
    secret = ndb.StringProperty()
    status = ndb.BooleanProperty()
    data = ndb.DateTimeProperty(auto_now_add=True)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return render_template('index.html')

@app.route('/update/<id>', methods=['POST'])
def updateQuestion(id=None):
    try:
        keyID = int(id)
    except:
        return 'Invalid key'

    questionKey = ndb.Key('Question', keyID)
    storedQuestion = questionKey.get()

    if storedQuestion is None:
        return 'Question not found'

    secret = request.form['secret']
    if storedQuestion.secret != secret:
        return 'Invalid secret'

    storedQuestion.text = request.form['question_text']

    if 'status' in request.form:
        storedQuestion.status = True
    else:
        storedQuestion.status = False

    storedQuestion.put()

    return render_template('success.html',
            id=questionKey.id(),
            status=storedQuestion.status,
            text=storedQuestion.text,
            secret=storedQuestion.secret)




@app.route('/create', methods=['POST'])
def createQuestion():
    error = None
    questionText = request.form['question_text']

    question = Question()
    question.text = questionText
    question.secret = base64.urlsafe_b64encode(urandom(24))
    questionKey = question.put()

    return render_template('success.html',
            id=questionKey.id(),
            status=question.status,
            text=question.text,
            secret=question.secret)


@app.route('/<id>/<secret>', methods=['GET'])
def editQuestion(id=None, secret=None):
    try:
        keyID = int(id)
    except:
        return 'Invalid key'

    questionKey = ndb.Key('Question', keyID)
    storedQuestion = questionKey.get()

    if storedQuestion is None:
        return 'Question not found'

    if storedQuestion.secret != secret:
        return 'Invalid secret'

    return render_template('edit.html',
            id=questionKey.id(),
            status=storedQuestion.status,
            text=storedQuestion.text,
            secret=storedQuestion.secret)


@app.route('/<id>', methods=['GET'])
def showQuestion(id=None):
    try:
        keyID = int(id)
    except:
        return 'not a valid key'

    questionKey = ndb.Key('Question', keyID)
    storedQuestion = questionKey.get()

    if storedQuestion is None:
        return 'Could\'t find question'

    return str(storedQuestion)



@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
