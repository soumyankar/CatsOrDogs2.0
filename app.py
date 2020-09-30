from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__) #Indexing root folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # 3 forward slashes means relative path; 4 forward slashes means exact path
db = SQLAlchemy(app)

class Participants(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	weblink = db.Column(db.String(2000), nullable=False)
	name = db.Column(db.String(200),nullable=False)
	breed = db.Column(db.String(200), nullable=False)
	mean = db.Column(db.Float(), nullable=False)
	deviation = db.Column(db.Float(),nullable=False)
	history = db.Column(db.String(20000), nullable=True)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return '<Participant %r>' % self.id

@app.route('/', methods=['POST','GET'])
def index():
	return render_template('index.html')

	if __name__ == "main":
		app.run(debug=True)


@app.route('/participants/', methods=['GET','POST'])
def participants():
	animals = Participants.query.all()
	return render_template('participants.html',animals=animals)
