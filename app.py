# flask imports
from flask import Flask, Response, render_template, request, redirect, url_for

# flask setup
app = Flask(__name__)
app.config["SECRET_KEY"] = "ITSASECRET"

# flask-login imports
from flask_login import LoginManager
from flask_login import login_required, current_user 
from login import login_manager, login_handler, logout_handler
login_manager.init_app(app)

# SQLAlchemy

from model import Base,User,Post
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///project.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/')
def hello_world():
    posts=session.query(Post).order_by("id desc").all()  
    return render_template('home.html')

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


@app.route('/Category/Boys')
def Clothes():
	posts=session.query(Post).filter_by(category="Clothes").all()
	return render_template('lifehacxcat.html' ,posts=posts)

@app.route('/Category/Girls')
def Garden():
	posts=session.query(Post).filter_by(category="Garden").all()
	return render_template('lifehacxcat.html',posts=posts)

@app.route('/Category/Both')
def Food():
	posts=session.query(Post).filter_by(category="Food").all()
	return render_template('lifehacxcat.html', posts=posts)

@app.route('/Category/Young')
def Makeup():
	posts=session.query(Post).filter_by(category="Makeup").all()
	return render_template('lifehacxcat.html', posts=posts)

@app.route('/Category/Old')
def Home_Design():
	posts=session.query(Post).filter_by(category="Home_Design").all()
	return render_template('lifehacxcat.html',posts=posts)

@app.route('/Category/Others')
def Camping():
	posts=session.query(Post).filter_by(category="Camping").all()
	return render_template('lifehacxcat.html',posts=posts)

@app.route('/Category/Stories')
def Other():
	posts=session.query(Post).filter_by(category="Other").all()
	return render_template('lifehacxcat.html', posts=posts)

@app.route('/Add_Hack', methods=["GET", "POST"])
def Add_Hack():
	if request.method == "GET":
		#show the webpage
		return render_template('Add_Hack.html')	
	if request.method == "POST":
		vid_url = request.form.get("vid_url")
		title = request.form.get("title")
		category = request.form.get("category")
		description = request.form.get("description")

		embed_video = vid_url
		
		vid_url = 'https://youtube.com/embed/'+ embed_video.split('=')[1]

		new_post = Post(title=title, description=description,
			video_url=vid_url,category=category)
		session.add(new_post)
		session.commit()
		return redirect(url_for('hello_world'))

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


'''
	THINGS IN A POST

	title = Column(Text (50))
 	description = Column(String(1000))
 	video_url = Column(String(500))
 	category = Column(String(20))


 	BACKEND HTML

	title
	category
	vid_url
	description

 	'''
