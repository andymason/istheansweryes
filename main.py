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
    data = ndb.DateTimeProperty(auto_now_add=True)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def createQuestion():
    error = None
    questionText = request.form['question_text']

    question = Question()
    question.text = questionText
    question.secret = base64.urlsafe_b64encode(urandom(24))
    questionKey = question.put()

    return render_template('success.html', id=questionKey.id(), secret=question.secret)

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
