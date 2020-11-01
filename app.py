# For printing to console.
from __future__ import print_function
import sys

from flask import Flask,flash,render_template,url_for,request,redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from sqlalchemy import asc, desc
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from trueskill import Rating, quality_1vs1, rate_1vs1
import os

app = Flask(__name__) #Indexing root folder
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False;
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') # os.environ.get('DATABASE_URL') #sqlite:///test.db' # 3 forward slashes means relative path; 4 forward slashes means exact path
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin'
Hero = None # Hero Dog
selectedDog = None # Global variable that holds the dog in battleDog
selectedCat = None # Global variable that holds the cat in battleCat
battleOrder = [] # Global variable that holds order of battle
battleWinner = [] # Global variable that holds order of battle winners
iterations = 0 # Global variable that keeps count of 10 iterations.
labratID = -99 # Global variable that holds the ID of the next user to be added
labratName = "My mentors dont help me sadkek" # Global variable that holds labrat's name

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
	hero=db.Column(db.Integer)
	battle_order=db.Column(db.String(100),unique=False)
	battle_winner=db.Column(db.String(100),unique=False)
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
@app.route('/battle', methods=['POST','GET'])
def battle():
	dogs=Dogs.query.all()
	return render_template('battle.html',dogs=dogs)

def FindMatch(battleDog):
	global battleOrder, iterations, selectedDog, selectedDogTS
	cats = Cats.query.all()
	battleDogTrueSkill = battleDog
	# lowerLimit = battleDogMean - 2*battleDogDeviation
	# upperLimit = battleDogMean + 2*battleDogDeviation
	bestRating = 99999
	for cat in cats: # Going through all our cats because do not have many cats, but originally only loop from (mu-2*sigma) to (mu+2*sigma)
		catMean = cat.mean
		catDeviation = cat.deviation
		tempCatTrueSkill = Rating(mu = catMean,sigma = catDeviation)
		tempQuality = quality_1vs1(battleDogTrueSkill,tempCatTrueSkill)
		if cat.id in battleOrder:
			continue
		if (abs(tempQuality - 50) < bestRating): # Finding closest matchup, i.e 50% draw prob. and checking if (i) has been selected already
			bestRating = abs(tempQuality - 50)
			bestCat = cat # Best Match yet (this is dataclip)
	battleOrder.append(bestCat.id)
	print('battleOrder =',battleOrder,file=sys.stderr)
	print('Best Cat =',bestCat.id,',',bestCat.mean,file=sys.stderr)
	iterations = iterations + 1
	return bestCat

@app.route('/battlesetup',methods=['POST'])
def battlesetup():
	global selectedDog,iterations,battleWinner, battleOrder, selectedDogTS
	if request.form['animalType'] == "dog":
		battleWinner.append(int(1))
		tCat = Rating(mu = (Cats.query.get_or_404(battleOrder[-1])).mean, sigma = (Cats.query.get_or_404(battleOrder[-1])).deviation)
		selectedDogTS,x = rate_1vs1(selectedDogTS, tCat)
		print(selectedDogTS)
	if request.form['animalType'] == "cat":
		battleWinner.append(int(0))
		tCat = Rating(mu = (Cats.query.get_or_404(battleOrder[-1])).mean, sigma = (Cats.query.get_or_404(battleOrder[-1])).deviation)
		x,selectedDogTS = rate_1vs1(tCat, selectedDogTS)
		print(selectedDogTS)
	if iterations > 4:
		print('battleOrder = ',battleOrder, file=sys.stderr)
		print('battleWinner = ',battleWinner, file=sys.stderr)
		battleDog = Dogs.query.get_or_404(request.form['selectedModel'])
		commitdata(battleDog,battleOrder,battleWinner)
		iterations = 0
		battleOrder = []
		battleWinner = []
		return jsonify({'gameover' : 'true', 'endText': 'All 5 tests over'})
	if iterations <=4:
		battleDog = Dogs.query.get_or_404(request.form['selectedModel'])
		if iterations == 0: # First iteration only
			selectedDog = Rating(mu = battleDog.mean, sigma = battleDog.deviation)
			selectedDogTS = selectedDog
			sDogTS = selectedDog
			Hero = battleDog
		if iterations > 0:
			sDogTS = selectedDogTS
		battleCat = FindMatch(sDogTS) # Always pass TrueSkill variable
		return jsonify({
		'catID': battleCat.id,
		'catName': battleCat.name,
		'catBreed': battleCat.breed,
		'catWeblink': battleCat.weblink,
		'dogID': battleDog.id,
		'dogName': battleDog.name,
		'dogBreed': battleDog.breed,
		'dogWeblink': battleDog.weblink,
		})

@app.route('/commitlabrat', methods=['POST'])
def commitlabrat():
	global labratID,labratName
	labratID = LabRats.query.count()
	labratID = labratID + 1
	if request.form['name']:
		labratName = request.form['name']
	return jsonify({'labrat': labratName})

def commitdata(sDog, bOrder, bWinner):
	global labratID
	# Commiting LabRat Info
	hero = sDog.id
	new_labrat=LabRats(name=labratName,hero=hero,battle_order=' '.join(map(str,bOrder)),battle_winner=' '.join(map(str,bWinner)))
	db.session.add(new_labrat)
	db.session.commit()
	# Commit The Battles
	DogTS = Rating(mu = sDog.mean, sigma = sDog.deviation)
	length = len(bOrder)
	for i in range(0,length):
		tCat = Cats.query.get_or_404(bOrder[i])
		CatTS = Rating(mu = tCat.mean, sigma = tCat.deviation)
		# Finding W/L status
		if bWinner[i] == 1:
			new_DogTS, new_CatTS = rate_1vs1(DogTS,CatTS)
			dogResult = "W"
			catResult = "L"
		if bWinner[i] == 0:
			new_DogTS, new_CatTS = rate_1vs1(CatTS,DogTS)
			dogResult = "L"
			catResult = "W"
		# Commiting all this data.
		bDog = Dogs.query.filter_by(id=sDog.id).first()
		# First we shall commit dogs.
		bDog.mean_history = bDog.mean_history+str(round(bDog.mean,3))+" "
		bDog.deviation_history = bDog.deviation_history+str(round(bDog.deviation,2))+" "
		bDog.mean = round(new_DogTS.mu,3)
		bDog.deviation = round(new_DogTS.sigma,2)
		bDogHistory = str(labratID)+" "+str(bOrder[i])+" "+str(round(tCat.mean,3))+" "+str(round(tCat.deviation,2))+" "+dogResult+" "
		bDog.battle_history = bDog.battle_history+""+bDogHistory
		# print(bDogHistory)
		# Now we shall commit cats
		bCat = Cats.query.filter_by(id=bOrder[i]).first()
		bCat.mean_history = bCat.mean_history+""+str(round(tCat.mean,3))+" "
		bCat.deviation_history = bCat.deviation_history+str(round(tCat.deviation,2))+" "
		bCat.mean = round(new_CatTS.mu,3)
		bCat.deviation = round(new_CatTS.sigma,2)
		bCatHistory = str(labratID)+" "+str(bDog.id)+" "+str(round(DogTS.mu,3))+" "+str(round(DogTS.sigma,2))+" "+catResult+" "
		bCat.battle_history = bCat.battle_history+""+bCatHistory
		db.session.commit()
		DogTS = new_DogTS

@app.route('/admin/labrats',methods=['GET'])
@login_required
def labrats():
	labrats = LabRats.query.all()
	return render_template('labrats.html', labrats = labrats)

@app.route('/admin/participants', methods=['GET','POST'])
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
			new_dog=Dogs(name=animal_name,breed=animal_breed,weblink=animal_weblink,mean=animal_mean,deviation=animal_deviation,mean_history="",deviation_history="",battle_history="")
			try:
				db.session.add(new_dog)
				db.session.commit()
				return redirect(url_for('participants'))
			except:
				return 'There was some error uploading dogs.'
		if(animal_type=='Cats'):
			animal_mean=float(request.form['rating'])
			animal_deviation=float(round((animal_mean/3),2))
			new_cat=Cats(name=animal_name,breed=animal_breed,weblink=animal_weblink,mean=animal_mean,deviation=animal_deviation,mean_history="",deviation_history="",battle_history="")
			try:
				db.session.add(new_cat)
				db.session.commit()
				return redirect(url_for('participants'))
			except:
				return 'There was some error uploading cats.'

	dogs = Dogs.query.all()
	cats = Cats.query.all()
	return render_template('participants.html',dogs=dogs, cats=cats)

@app.route('/admin/participants/delete-dogs/<int:id>')
@login_required
def delete_dogs(id):
	dog_to_delete= Dogs.query.get_or_404(id)
	try:
		db.session.delete(dog_to_delete)
		db.session.commit()
		return redirect('/participants')
	except:
		return 'Couldnt delete lol'

@app.route('/admin/participants/delete-cats/<int:id>')
@login_required
def delete_cats(id):
	cat_to_delete= Cats.query.get_or_404(id)
	try:
		db.session.delete(cat_to_delete)
		db.session.commit()
		return redirect('/participants')
	except:
		return 'Couldnt delete lol'

@app.route('/admin/participants/trueskill-dogs/<int:id>')
@login_required
def trueskill_dog(id):
	dog = Dogs.query.get_or_404(id)
	LabRatID = []
	OpponentName =[]
	OpponentMean = []
	OpponentDeviation = []
	labels = []
	Result = []
	MeanHistory = list(map(float,map(str,dog.mean_history.split())))
	DeviationHistory = list(map(float,map(str,dog.deviation_history.split())))
	i = 0
	length = 0
	Parse = dog.battle_history.split()
	for x in Parse:
		if i >= 5:
			i = 0
		if i==0:
			LabRatID.append(x.encode('ascii','ignore'))
		if i==1:
			OpponentName.append(str((Cats.query.get_or_404(int((x.encode('ascii','ignore').decode('UTF-8')))).name)))
		if i==2:
			OpponentMean.append(float(str(x.encode('ascii','ignore').decode('UTF-8'))))
		if i==3:
			OpponentDeviation.append(float(str(x.encode('ascii','ignore').decode('UTF-8'))))
		if i==4:
			Result.append(str(x.encode('ascii','ignore').decode('UTF-8')))
		i = i + 1
	length = len(LabRatID)
	OpponentMean = list(OpponentMean)
	OpponentDeviation = list(OpponentDeviation)
	for i in range(0,length):
		labels.append(i)
	return render_template('trueskill.html',labels=labels, animal = dog, MeanHistory = MeanHistory,DeviationHistory = DeviationHistory,LabRatID = LabRatID, OpponentName = OpponentName, OpponentMean = OpponentMean, OpponentDeviation = OpponentDeviation, Result = Result, length=length)

@app.route('/admin/participants/trueskill-cats/<int:id>')
@login_required
def trueskill_cat(id):
	cat = Cats.query.get_or_404(id)
	LabRatID = []
	OpponentName =[]
	OpponentMean = []
	OpponentDeviation = []
	Result = []
	labels = []
	MeanHistory = list(map(float,map(str,cat.mean_history.split())))
	DeviationHistory = list(map(float,map(str,cat.deviation_history.split())))
	i = 0
	length = 0
	Parse = cat.battle_history.split()
	for x in Parse:
		if i >= 5:
			i = 0
		if i==0:
			LabRatID.append(x.encode('ascii','ignore'))
		if i==1:
			OpponentName.append(str((Dogs.query.get_or_404(int((x.encode('ascii','ignore').decode('UTF-8')))).name)))
		if i==2:
			OpponentMean.append(float(str(x.encode('ascii','ignore').decode('UTF-8'))))
		if i==3:
			OpponentDeviation.append(float(str(x.encode('ascii','ignore').decode('UTF-8'))))
		if i==4:
			Result.append(str(x.encode('ascii','ignore').decode('UTF-8')))
		i = i + 1
	length = len(LabRatID)
	OpponentMean = list(OpponentMean)
	OpponentDeviation = list(OpponentDeviation)
	for i in range(0,length):
		labels.append(i)
	return render_template('trueskill.html',animal = cat, labels = labels, MeanHistory = MeanHistory,DeviationHistory = DeviationHistory,LabRatID = LabRatID, OpponentName = OpponentName, OpponentMean = OpponentMean, OpponentDeviation = OpponentDeviation, Result = Result, length=length)
