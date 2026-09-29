from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError

# def validate_email_domain(allowed_domain):
#     def _validate(form, field):
#         email = field.data
#         if '@' not in email:
#             return  # let Email() catch malformed addresses
#         domain = email.rsplit('@', 1)[1].lower()
#         if domain != allowed_domain and not domain.endswith('.' + allowed_domain):
#             raise ValidationError(f'Email must be from the {allowed_domain} domain.')
#     return _validate

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    # email = StringField(
    #     'What is your UofT email?',
    #     validators=[Email(), DataRequired(), validate_email_domain('utoronto.ca')])
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
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        # session['email'] = form.email.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)