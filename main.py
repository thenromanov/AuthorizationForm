from flask import Flask, render_template, redirect, request, abort
from flask_wtf import FlaskForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from wtforms import IntegerField, StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import EmailField, DateTimeLocalField
from wtforms.validators import DataRequired, InputRequired
from data import dbSession
from data.users import User
from data.jobs import Jobs
from data.departments import Department
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
    teamLeader = IntegerField('Team Leader', validators=[DataRequired()])
    job = StringField('Job', validators=[DataRequired()])
    workSize = IntegerField('Duration', validators=[DataRequired()])
    collaborators = StringField('Collaborators', validators=[DataRequired()])
    startDate = DateTimeLocalField('Start Date', format='%Y-%m-%dT%H:%M',
                                   validators=[InputRequired()], default=datetime.datetime.now())
    endDate = DateTimeLocalField('Finish Date', format='%Y-%m-%dT%H:%M',
                                 validators=[InputRequired()])
    isFinished = BooleanField('Is finished?')
    submit = SubmitField('Add Task')


class DepartmentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    chief = IntegerField('Chief', validators=[DataRequired()])
    members = StringField('Members', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Add department')


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
def addTask():
    form = JobsForm()
    if form.validate_on_submit():
        session = dbSession.createSession()
        job = Jobs(teamLeader=form.teamLeader.data, job=form.job.data, workSize=form.workSize.data,
                   collaborators=form.collaborators.data, startDate=form.startDate.data,
                   endDate=form.endDate.data, isFinished=form.isFinished.data)
        current_user.jobs.append(job)
        session.merge(current_user)
        session.commit()
        return redirect('/')
    return render_template('task.html', title='Task addition', form=form)


@app.route('/task/<int:id>', methods=['GET', 'POST'])
@login_required
def editTask(id):
    form = JobsForm()
    if request.method == 'GET':
        session = dbSession.createSession()
        job = session.query(Jobs).filter(Jobs.id == id, (Jobs.user ==
                                                         current_user) | (current_user.id == 1)).first()
        if job:
            form.teamLeader.data = job.teamLeader
            form.job.data = job.job
            form.workSize.data = job.workSize
            form.collaborators.data = job.collaborators
            form.startDate.data = job.startDate
            form.endDate.data = job.endDate
            form.isFinished.data = job.isFinished
        else:
            abort(404)
    if form.validate_on_submit():
        session = dbSession.createSession()
        job = session.query(Jobs).filter(Jobs.id == id, (Jobs.user ==
                                                         current_user) | (current_user.id == 1)).first()
        if job:
            job.teamLeader = form.teamLeader.data
            job.job = form.job.data
            job.workSize = form.workSize.data
            job.collaborators = form.collaborators.data
            job.startDate = form.startDate.data
            job.endDate = form.endDate.data
            job.isFinished = form.isFinished.data
            session.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('task.html', title='Task Edition', form=form)


@app.route('/task_remove/<int:id>', methods=['GET', 'POST'])
@login_required
def removeTask(id):
    session = dbSession.createSession()
    job = session.query(Jobs).filter(Jobs.id == id, (Jobs.user == current_user)
                                     | (current_user.id == 1)).first()
    if job:
        session.delete(job)
        session.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/department', methods=['GET', 'POST'])
@login_required
def addDepartment():
    form = DepartmentForm()
    if form.validate_on_submit():
        session = dbSession.createSession()
        department = Department(title=form.title.data, chief=form.chief.data, members=form.members.data,
                                email=form.email.data)
        current_user.departments.append(department)
        session.merge(current_user)
        session.commit()
        return redirect('/departments')
    return render_template('department.html', title='Department addition', form=form)


@app.route('/department/<int:id>', methods=['GET', 'POST'])
@login_required
def editDepartment(id):
    form = DepartmentForm()
    if request.method == 'GET':
        session = dbSession.createSession()
        department = session.query(Department).filter(Department.id == id, (Department.user == current_user)
                                                      | (current_user.id == 1)).first()
        if department:
            form.title.data = department.title
            form.chief.data = department.chief
            form.members.data = department.members
            form.email.data = department.email
        else:
            abort(404)
    if form.validate_on_submit():
        session = dbSession.createSession()
        department = session.query(Department).filter(Department.id == id, (Department.user == current_user)
                                                      | (current_user.id == 1)).first()
        if department:
            department.title = form.title.data
            department.chief = form.chief.data
            department.members = form.members.data
            department.email = form.email.data
            session.commit()
            return redirect('/departments')
    return render_template('department.html', title='Department edition', form=form)


@app.route('/department_remove/<int:id>', methods=['GET', 'POST'])
@login_required
def removeDepartment(id):
    session = dbSession.createSession()
    department = session.query(Department).filter(Department.id == id, (Department.user == current_user)
                                                  | (current_user.id == 1)).first()
    if department:
        session.delete(department)
        session.commit()
    else:
        abort(404)
    return redirect('/departments')


@app.route('/departments')
def departmentsPage():
    session = dbSession.createSession()
    users = session.query(User).all()
    departments = session.query(Department).all()
    return render_template('departments.html', users=users, departments=departments)


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
