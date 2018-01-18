# flask imports
from flask import Flask, Response, render_template, request, redirect, url_for
import uuid

from flask_sqlalchemy import SQLAlchemy

# flask setup
app = Flask(__name__)
app.config["SECRET_KEY"] = "ITSASECRET"
db=SQLAlchemy(app)

# flask-login imports
from flask_login import LoginManager
from flask_login import login_required, current_user 


from create_db import Links, Base

# SQLAlchemy


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///./project.db')
Base.metadata.bind = engine
Base.metadata.create_all(bind=engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
login_manager = LoginManager()
login_manager.init_app(app)


def my_random_string(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4()) # Convert UUID format to a Python string.
    random = random.upper() # Make all characters uppercase.
    random = random.replace("-","") # Remove the UUID '-'.
    return random[0:string_length] # Return the random strin



def random_letters():
	shortened_link = ""
	if request.form['spl'] == "":
		
		shortened_link= my_random_string()
		
	else:
		shortened_link = request.form['spl']

	return shortened_link



@app.route('/' , methods=['GET', 'POST'])
def home():

	if request.method == "GET":
		#show the webpage
		print "This is GET"
		return render_template('home.html')	
	elif request.method=="POST":
		print "This is post"

		

		
		link= Links(request.form['user'],request.form['original_link'],random_letters())
		db.session.add(link)

		
		
		db.session.commit()
		print "committed"
		
		
		

		
		return redirect(url_for('home'))





		

@app.route('/login', methods=['GET', 'POST'])
def login():
    return login_handler(request)


@app.route('/logout')
def logout():
  return logout_handler()


@app.route('/protected', methods=["GET"])
@login_required
def protected():

    return render_template('protected.html')



		# redirect
@app.route('/', methods=["GET","POST"])
def Add_user():	
	if request.method == "GET":
		return render_template('index.html')

	else:
		first_name = request.form.get("first_name")
		last_name = request.form.get("last_name")
		user_name = first_name + " " +last_name
		email = request.form.get("email")
		psw = request.form.get("psw")

		new_user = User(first_name=first_name, last_name=last_name, user_name=user_name, email=email,
			psw_hash=psw)
		return redirect(url_for('hello_world'))


@login_manager.user_loader
def load_user(user_id):
	return User.get(user_id)

@app.route('/login_form', methods=['GET', 'POST'])
def login_form():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
	form = LoginForm()
	if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
		login_user(user)

		flask.flash('Logged in successfully.')

		next = flask.request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
		if not is_safe_url(next):
			return flask.abort(400)

		return flask.redirect(next or flask.url_for('index'))
	return flask.render_template('login.html', form=form)

app.run(debug=True)



