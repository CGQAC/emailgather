from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = '1234123412341234'
db = SQLAlchemy(app)


class EmailForm(FlaskForm):
	first_name = StringField('First Name',
		validators=[
			DataRequired(),
			Length(min=1, max=100)
		])
	last_name = StringField('Last Name',
		validators=[
			DataRequired(),
			Length(min=1, max=100)
		])
	email = StringField('Email',
		validators=[
			DataRequired(),
			Email()
		])
	submit = SubmitField('Submit')

class Emails(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(100), nullable=False, unique=False)
	last_name = db.Column(db.String(100), nullable=False, unique=False)
	email = db.Column(db.String(150), nullable=False, unique=True)

	def __repr__(self):
		return ''.join(['ID : ', self.id, '\r\n', 'Name: ', self.first_name, self.last_name, '\r\n', 'Email: ', self.email])

@app.route('/', methods=['GET', 'POST'])
def home():
	form = EmailForm()
	if form.validate_on_submit():
		f = form.first_name.data
		l = form.last_name.data
		e = form.email.data
		formData = Emails(first_name=f, last_name=l, email=e)		
		db.session.add(formData)
		db.session.commit()
		return redirect(url_for('list'))
	return render_template('post.html', form=form)

@app.route('/list')
def list():
	emails = Emails.query.all()
	return render_template('list.html', emails=emails)
