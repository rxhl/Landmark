from flask import Flask, render_template, request, session, redirect, url_for
from models import db, User, Place
from forms import SignupForm, LoginForm, AddressForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', db_local)
db.init_app(app)

app.secret_key = "07943d11821d591695c6232c4076b120b3d48627415a398373d9fca2aeacce4c"

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/signup", methods = ['GET', 'POST']) # Differentiate between GET and POST
def signup():
	if 'email' in session:
		return redirect(url_for('home'))
	
	form = SignupForm()
	
	if request.method == 'POST':
		if form.validate() == False:
			return render_template("signup.html", form = form)
		else:
			newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
			db.session.add(newuser)
			db.session.commit()
			
			# To start a new session
			session['email'] = newuser.email
			return redirect(url_for('home'))
	
	elif request.method == "GET":
		return render_template("signup.html", form = form)
	
@app.route("/login", methods = ['GET', 'POST'])
def login():
	if 'email' in session:
		return redirect(url_for('home'))
	
	form = LoginForm()
	
	if request.method == 'POST':
		if form.validate() == False:
			return render_template("login.html", form = form)
		else:
			email = form.email.data
			password = form.password.data
			
			# Check if the user exists in the database
			
			user = User.query.filter_by(email = email).first()
			if user is not None and user.check_password(password):
				session['email'] = form.email.data
				return redirect(url_for('home'))
			else:
				return redirect(url_for('login'))
	elif request.method == 'GET':
		return render_template('login.html', form=form)
		
@app.route("/logout")
def logout():
	# Delete the cookie
	session.pop('email', None)
	return redirect(url_for('index'))
	
	
@app.route("/home", methods = ['GET', 'POST'])
def home():
	if 'email' not in session:
		return redirect(url_for('login')) # Protecting unauthorized access to home.
		
	form = AddressForm()
	
	places = []
	my_coordinates = (37.4221, -122.0844)
	
	if request.method == 'POST':
		if form.validate == False:
			return render_template("home.html", form=form)
		else:
			# 1. Get the address
			address = form.address.data
			
			# 2. Query for places around it
			p = Place()
			my_coordinates = p.address_to_latlng(address)
			places = p.query(address)
			
			# 3. Return the results
			return render_template("home.html", form=form, my_coordinates=my_coordinates, places=places)
	
	elif request.method == 'GET': 
		return render_template("home.html", form=form, my_coordinates=my_coordinates, places=places)

if __name__ == "__main__":
	app.run(debug = True)