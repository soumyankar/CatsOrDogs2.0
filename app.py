from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__) #Indexing root folder
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # 3 forward slashes means relative path; 4 forward slashes means exact path
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'my mentors dont help me sadkek'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin'

class Admin(UserMixin, db.Model):
	id=db.Column(db.Integer, primary_key=True)
	username=db.Column(db.String(15),unique=True)
	email=db.Column(db.String(80),unique=True)
	password=db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
	return Admin.query.get((user_id))

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

@app.route('/', methods=['POST','GET'])
def index():
	return render_template('index.html')

	if __name__ == "main":
		app.run(debug=True)


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
			new_dog=Dogs(name=animal_name,breed=animal_breed,weblink=animal_weblink,mean=animal_mean,deviation=animal_deviation,mean_history=animal_mean,deviation_history=animal_deviation,battle_history="NULL ")
			try:
				db.session.add(new_dog)
				db.session.commit()
				return redirect(url_for('participants'))
			except:
				return 'There was some error uploading dogs.'
		if(animal_type=='Cats'):
			animal_mean=float(request.form['rating'])
			animal_deviation=float(animal_mean/3)
			new_cat=Cats(name=animal_name,breed=animal_breed,weblink=animal_weblink,mean=animal_mean,deviation=animal_deviation,mean_history=animal_mean,deviation_history=animal_deviation,battle_history="NULL ")
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
def delete_dogs(id):
	dog_to_delete= Dogs.query.get_or_404(id)
	try:
		db.session.delete(dog_to_delete)
		db.session.commit()
		return redirect('/participants')
	except:
		return 'Couldnt delete lol'

@app.route('/participants/delete-cats/<int:id>')
def delete_cats(id):
	cat_to_delete= Cats.query.get_or_404(id)
	try:
		db.session.delete(cat_to_delete)
		db.session.commit()
		return redirect('/participants')
	except:
		return 'Couldnt delete lol'

@app.route('/participants/trueskill-dogs/<int:id>')
def trueskill_dog(id):
	dog = Dogs.query.get_or_404(id)
	return render_template('trueskill.html',animal = dog)

@app.route('/participants/trueskill-cats/<int:id>')
def trueskill_cat(id):
	cat = Cats.query.get_or_404(id)
	return render_template('trueskill.html',animal = cat)
