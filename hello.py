import re
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError

def validate_uoft_domain(form, field):
    email = field.data
    if '@' not in email:
        return
    domain = email.rsplit('@', 1)[1].lower()
    if domain != 'utoronto.ca' and not domain.endswith('.utoronto.ca'):
        raise ValidationError('Please use your UofT email')

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField(
        'What is your UofT email?',
        validators=[Email(), DataRequired(), validate_uoft_domain])
    submit = SubmitField('Submit')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdf1234'
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        old_email = session.get('email')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your email!')
        session['name'] = form.name.data
        session['email'] = form.email.data
        return redirect(url_for('chat_page'))
    return render_template('index.html',
                           form=form,
                           name=session.get('name'),
                           email=session.get('email'))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.route('/chat')
def chat_page():
    # guard: must have a valid session (came through the form) to reach chat
    if not session.get('email'):
        return redirect(url_for('index'))
    return render_template('chat.html', name=session.get('name'))


@app.route('/chat', methods=['POST'])
def chat():
    message = request.json['message']
    reply = generate_reply(message)
    return {'reply': reply}


def generate_reply(message):
    lower = message.lower()

    # remember a name if the user tells us one
    match = re.search(r"my name is (\w+)", lower)
    if match:
        remembered_name = match.group(1).capitalize()
        session['remembered_name'] = remembered_name
        return f"Nice to meet you, {remembered_name}!"

    # recall it later
    if "what is my name" in lower or "what's my name" in lower:
        remembered_name = session.get('remembered_name')
        if remembered_name:
            return f"Your name is {remembered_name}."
        return "I don't know your name yet — tell me!"

    if "hello" in lower:
        return "Hello!"

    return "I don't understand."


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))