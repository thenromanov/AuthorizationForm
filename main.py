from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from wtforms import IntegerField, StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import EmailField, DateTimeLocalField
from wtforms.validators import DataRequired, InputRequired
from data import dbSession
from data.users import User
from data.jobs import Jobs
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

loginManager = LoginManager()
loginManager.init_app(app)


class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    passwordRepeat = PasswordField('Password repeat', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Send')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    rememberMe = BooleanField('Remember me')
    submit = SubmitField('Login')


class JobsForm(FlaskForm):
    job = StringField('Job', validators=[DataRequired()])
    workSize = IntegerField('Duration', validators=[DataRequired()])
    collaborators = StringField('Collaborators', validators=[DataRequired()])
    startDate = DateTimeLocalField('Start Date', format='%Y-%m-%dT%H:%M',
                                   validators=[InputRequired()], default=datetime.datetime.now())
    endDate = DateTimeLocalField('Finish Date', format='%Y-%m-%dT%H:%M',
                                 validators=[InputRequired()])
    submit = SubmitField('Add Task')


@loginManager.user_loader
def loadUser(userId):
    session = dbSession.createSession()
    return session.query(User).get(userId)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.passwordRepeat.data:
            return render_template('register.html', title='Register', form=form, message='Different passwords')
        session = dbSession.createSession()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Register', form=form, message='User already exists')
        user = User(email=form.email.data, surname=form.surname.data, name=form.name.data,
                    age=form.age.data, position=form.position.data, speciality=form.speciality.data,
                    address=form.address.data)
        user.setPassword(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/')
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = dbSession.createSession()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.checkPassword(form.password.data):
            login_user(user, remember=form.rememberMe.data)
            return redirect('/')
        return render_template('login.html', form=form, title='Login', message='Wrong email or password')
    return render_template('login.html', form=form, title='Login')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/task', methods=['GET', 'POST'])
@login_required
def task():
    form = JobsForm()
    if form.validate_on_submit():
        session = dbSession.createSession()
        job = Jobs(teamLeader=current_user.id, job=form.job.data, workSize=form.workSize.data,
                   collaborators=form.collaborators.data, startDate=form.startDate.data,
                   endDate=form.endDate.data, isFinished=False)
        session.add(job)
        session.commit()
        return redirect('/')
    return render_template('task.html', title='Task addition', form=form)


@app.route('/')
def mainPage():
    session = dbSession.createSession()
    users = session.query(User).all()
    jobs = session.query(Jobs).all()
    return render_template('jobs.html', users=users, jobs=jobs)


def main():
    dbSession.globalInit('db/MarsOne.sqlite')
    app.run()


if __name__ == '__main__':
    main()
