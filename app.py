# For printing to console.
from __future__ import print_function
import sys

from flask import Flask,flash,render_template,url_for,request,redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from trueskill import Rating, quality_1vs1, rate_1vs1
import os

app = Flask(__name__) #Indexing root folder
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False;
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # os.environ.get('DATABASE_URL') #sqlite:///test.db' # 3 forward slashes means relative path; 4 forward slashes means exact path
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin'
selectedDog = ""
battleOrder = []
battleWinner = []
iterations = 0

class Admin(UserMixin, db.Model):
	id=db.Column(db.Integer, primary_key=True)
	username=db.Column(db.String(15),unique=True)
	email=db.Column(db.String(80),unique=True)
	password=db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
	return Admin.query.get((user_id))

class LabRats(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	name=db.Column(db.String(100),unique=False)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return '<LabRat %r>' % self.id

class Dogs(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200),nullable=False)
	breed = db.Column(db.String(200), nullable=False)
	weblink = db.Column(db.String(2000), nullable=False)
	mean = db.Column(db.Float(), nullable=False)
	deviation = db.Column(db.Float(),nullable=False)
	mean_history = db.Column(db.String(20000), nullable=True)
	deviation_history = db.Column(db.String(20000), nullable=True)
	battle_history = db.Column(db.String(20000),nullable=True)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return '<dogs %r>' % self.id

class Cats(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200),nullable=False)
	breed = db.Column(db.String(200), nullable=False)
	weblink = db.Column(db.String(2000), nullable=False)
	mean = db.Column(db.Float(), nullable=False)
	deviation = db.Column(db.Float(),nullable=False)
	mean_history = db.Column(db.String(20000), nullable=True)
	deviation_history = db.Column(db.String(20000), nullable=True)
	battle_history = db.Column(db.String(20000),nullable=True)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return '<cats %r>' % self.id

class LoginForm(FlaskForm):
	username = StringField('username', validators=[InputRequired()])
	password = PasswordField('password', validators=[InputRequired()])

@app.route('/admin',methods=['POST','GET'])
def admin():
	if current_user.is_authenticated:
		return redirect(url_for('participants'))
		flash('You are already logged in my dude')
	form = LoginForm()
	if form.validate_on_submit():
		user = Admin.query.filter_by(username=form.username.data).first()
		if user:
			if user.password == form.password.data:
				login_user(user,remember=False)
				return redirect(url_for('participants'))
			else:
				return '<h1>Wrong Password</h1>'
		else:
			return '<h1>Username or password is invalid.</h1>'
	return render_template('admin.html', form = form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/', methods=['POST','GET'])
def index():
	return render_template('index.html')

	if __name__ == "main":
		app.run(debug=True)

# Battle Page
@app.route('/battleform', methods=['POST','GET'])
def battleform():
	dogs = Dogs.query.all()
	global selectedDog
	if request.method == 'POST':
		selectedDog=request.form['selectedDog']
		return redirect(url_for('battle',selectedDog=selectedDog))
	# print('Hello world!', file=sys.stderr)
	return render_template('battleform.html', dogs=dogs)

@app.route('/battle', methods=['POST','GET'])
def battle():
	if iterations > 9:
		return jsonify({'gameover' : 'true', 'endText': 'All 10 tests over'})
	print('selectedDog =',selectedDog, file=sys.stderr)
	battle_dog = Dogs.query.get_or_404(selectedDog)
	cats = Cats.query.all()
	cats_mean = []
	cats_deviation = []
	for cat in cats:
		cats_mean.append(cat.mean)
		cats_deviation.append(cat.deviation)
	# print(cats_mean, file=sys.stderr)
	# print(cats_deviation, file=sys.stderr)
	return render_template('battle.html', battle_dog=battle_dog)

@app.route('/battlehandler',methods=['POST'])
def battlehandler():
	global battleOrder, battleWinner, iterations
	if iterations > 9:
			print('battleOrder = ',battleOrder, file=sys.stderr)
			print('battleWinner = ',battleWinner, file=sys.stderr)
			return jsonify({'gameover' : 'true', 'endText': 'All 10 tests over'})
	iterations = iterations + 1
	selectedModel = request.form['selectedModel']
	animalType = request.form['animalType']
	opponentCat = request.form['opponentCat']
	print('iterations =',iterations, file=sys.stderr)
	print('selectedModel = ',selectedModel, file=sys.stderr)
	print('animalType =',animalType, file=sys.stderr)
	print('opponentCat =',opponentCat, file=sys.stderr)
	if animalType == "dog":
		battleOrder.append(opponentCat)
		battleWinner.append(1)
	if animalType == "cat":
		battleOrder.append(opponentCat)
		battleWinner.append(0)
	if selectedModel:
		return jsonify({'selectedModel': selectedModel, 'animalType': animalType})
	else:
		return jsonify({'error': 'Missing data!'})

@app.route('/participants', methods=['GET','POST'])
@login_required
def participants():
	if request.method == 'POST':
		animal_name=request.form['name']
		animal_breed=request.form['breed']
		animal_weblink=request.form['weblink']
		animal_type=request.form['animaltype']
		if(animal_type=='Dogs'):
			animal_mean=float(25)
			animal_deviation=float(8.3)
			new_dog=Dogs(name=animal_name,breed=animal_breed,weblink=animal_weblink,mean=animal_mean,deviation=animal_deviation,mean_history=animal_mean,deviation_history=animal_deviation,battle_history="")
			try:
				db.session.add(new_dog)
				db.session.commit()
				return redirect(url_for('participants'))
			except:
				return 'There was some error uploading dogs.'
		if(animal_type=='Cats'):
			animal_mean=float(request.form['rating'])
			animal_deviation=float(animal_mean/3)
			new_cat=Cats(name=animal_name,breed=animal_breed,weblink=animal_weblink,mean=animal_mean,deviation=animal_deviation,mean_history=animal_mean,deviation_history=animal_deviation,battle_history="")
			try:
				db.session.add(new_cat)
				db.session.commit()
				return redirect(url_for('participants'))
			except:
				return 'There was some error uploading cats.'

	dogs = Dogs.query.all()
	cats = Cats.query.all()
	return render_template('participants.html',dogs=dogs, cats=cats)

@app.route('/participants/delete-dogs/<int:id>')
@login_required
def delete_dogs(id):
	dog_to_delete= Dogs.query.get_or_404(id)
	try:
		db.session.delete(dog_to_delete)
		db.session.commit()
		return redirect('/participants')
	except:
		return 'Couldnt delete lol'

@app.route('/participants/delete-cats/<int:id>')
@login_required
def delete_cats(id):
	cat_to_delete= Cats.query.get_or_404(id)
	try:
		db.session.delete(cat_to_delete)
		db.session.commit()
		return redirect('/participants')
	except:
		return 'Couldnt delete lol'

@app.route('/participants/trueskill-dogs/<int:id>')
@login_required
def trueskill_dog(id):
	dog = Dogs.query.get_or_404(id)
	return render_template('trueskill.html',animal = dog)

@app.route('/participants/trueskill-cats/<int:id>')
@login_required
def trueskill_cat(id):
	cat = Cats.query.get_or_404(id)
	return render_template('trueskill.html',animal = cat)
