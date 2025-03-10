"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

import os
from flask_wtf.csrf import generate_csrf
from flask.globals import session
from flask.helpers import flash
from flask_wtf import file
import jwt
import psycopg2
from sqlalchemy.sql.expression import desc 
from app import app, db, login_manager
from flask import request, jsonify, render_template,g,send_from_directory, send_file
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import  LoginForm, RegisterForm,carForm
from app.models import Users,Cars,Favourites
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
import datetime
from sqlalchemy.sql import func
from functools import wraps

###
# Routing for your application.
###
@app.route('/api/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})

def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    auth = request.headers.get('Authorization', None) # or request.cookies.get('token', None)

    if not auth:
      return jsonify({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}), 401

    parts = auth.split()

    if parts[0].lower() != 'bearer':
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}), 401
    elif len(parts) == 1:
      return jsonify({'code': 'invalid_header', 'description': 'Token not found'}), 401
    elif len(parts) > 2:
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'}), 401

    token = parts[1]
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])

    except jwt.ExpiredSignatureError:
        return jsonify({'code': 'token_expired', 'description': 'token is expired'}), 401
    except jwt.DecodeError:
        return jsonify({'code': 'token_invalid_signature', 'description': 'Token signature is invalid'}), 401

    g.current_user = user = payload
    return f(*args, **kwargs)

  return decorated

@app.route('/api/register', methods = ['POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit() and request.method=="POST":
        username = form.username.data
        password = form.password.data
        name = form.name.data
        email = form.email.data
        location = form.location.data
        biography = form.biography.data
        photo = form.photo.data
        date=datetime.datetime.now().strftime("%x %X")
        
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        user = Users(username=username, password=password, name=name, email=email, location=location, biography=biography, photo=filename,date_joined=date)
        db.session.add(user)
        db.session.commit()

        message = {
            "username": username,
            "name": name,
            "photo": filename,
            "email": email,
            "location": location,
            "biography": biography,
            "date_joined": date
        }
        return jsonify(message=message)
    
    else:
        errors = {
            "errors": form_errors(form)
        }
        return jsonify(errors=errors)

@app.route('/api/cars', methods = ['POST'])
@requires_auth
@login_required
def addcars():
    form = carForm()
    if form.validate_on_submit() and request.method=="POST":
        make = form.make.data
        model = form.model.data
        colour = form.colour.data
        year = form.year.data
        price = form.price.data
        ctype = form.ctype.data
        transmission = form.transmission.data
        description = form.description.data
        photo = form.photo.data
        
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        car = Cars(description=description, make=make, model=model, colour=colour, year=year, transmission=transmission, car_type=ctype, photo=filename,price=price,user_id=current_user.id)
        db.session.add(car)
        db.session.commit()

        message = {
            "user_id":current_user.id,
            "make": make,
            "model": model,
            "photo": filename,
            "car_type": ctype,
            "price": price,
            "description": description,
            "year": year,
            "colour":colour,
            'transmission':transmission,
        }
        
        return jsonify(message=message)
    
    else:
        errors = {
            "errors": form_errors(form)
        }
        return jsonify(errors=errors)


@app.route('/api/cars', methods = ['GET'])
@requires_auth
@login_required
def returncars():
    if request.method=="GET":
        allcars=Cars.query.order_by(desc(Cars.id)).limit(3).all()
        data=[]
        for i in allcars:
            data.append({
                'id':i.id,
                'description':i.description,
                'year':i.year,
                'make':i.make,
                'model':i.model,
                'colour':i.colour,
                'transmission':i.transmission,
                'car_type':i.car_type,
                'price':i.price,
                'photo':"/uploads/"+i.photo,
                'user_id':i.user_id
            })
        return jsonify(data=data)

@app.route('/api/search', methods = ['GET'])
@requires_auth
@login_required
def search():
    if request.method=="GET":
        make=request.args.get('make')
        model=request.args.get('model')
        if not make and not model:
            errors={
                'errors':['No results found!']
            }
            return jsonify(errors=errors)
        elif not make:
            query=db.session.query(Cars).filter_by(model=model).all()
        elif not model:
            query=db.session.query(Cars).filter_by(make=make).all()
        else:
            query=db.session.query(Cars).filter(Cars.make==make, Cars.model==model).all()
      
        if query == None or query == []:
            errors={
                'errors':['No results found!']
            }
            return jsonify(errors=errors)
        else:
            data=[]
            for i in query:
                data.append({
                    'id':i.id,
                    'description':i.description,
                    'year':i.year,
                    'make':i.make,
                    'model':i.model,
                    'colour':i.colour,
                    'transmission':i.transmission,
                    'car_type':i.car_type,
                    'price':i.price,
                    'photo':"/uploads/"+i.photo,
                    'user_id':i.user_id
                })

    return jsonify(data=data)


@app.route('/api/cars/<car_id>', methods=['GET'])
@requires_auth
@login_required
def getcardetails(car_id):
    if request.method == 'GET':
        cardata = db.session.query(Cars).filter_by(id=car_id).first()
        data={
            'id':cardata.id,
            'description':cardata.description,
            'year':cardata.year,
            'make':cardata.make,
            'model':cardata.model,
            'colour':cardata.colour,
            'transmission':cardata.transmission,
            'car_type':cardata.car_type,
            'price':cardata.price,
            'photo':"/uploads/"+cardata.photo,
            'user_id':cardata.user_id
        }
        return jsonify(data=data)
    errors={
        'errors': 'Method Not Allowed'
        }
    return  jsonify(errors)



@app.route('/api/cars/<car_id>/favourite', methods=['POST'])
@requires_auth
@login_required
def favorites(car_id):
    user_id = current_user.id
    query=db.session.query(Favourites).filter( Favourites.car_id==car_id,Favourites.user_id==user_id).all()

    if not query and request.method == 'POST':
        fav_car = Favourites(user_id,car_id) 
        db.session.add(fav_car) 
        db.session.commit()
        data={
            'message': "Car Successfully Favourited",
            "car_id": car_id
        }
        return jsonify(data=data)
    errors={
        'errors': ['Car is already a favourite!']
    }
    return jsonify(errors=errors)


@app.route('/api/users/<user_id>/favourites', methods=['GET'])
@requires_auth
@login_required
def userfavorites(user_id):
    if request.method == 'GET':
        query= db.session.query(Favourites).filter_by(user_id=user_id).all()
        if query==[] or query ==None:
            errors={
            'errors': ['You have no favorite cars!']
            }
            return jsonify(errors=errors)
        else:
            data=[]
            for i in query:
                favlist = db.session.query(Cars).filter(Cars.id==i.car_id).first()
                data.append({
                    'id':favlist.id,
                    'description':favlist.description,
                    'year':favlist.year,
                    'make':favlist.make,
                    'model':favlist.model,
                    'colour':favlist.colour,
                    'transmission':favlist.transmission,
                    'car_type':favlist.car_type,
                    'price':favlist.price,
                    'photo':"/uploads/"+favlist.photo,
                    'user_id':favlist.user_id
                })

        return jsonify(data=data)
    errors={
            'errors': ['Invalid Method!']
            }
    return jsonify(errors=errors)



@app.route('/api/users/<user_id>', methods=['GET'])
@requires_auth
@login_required
def getuserdetails(user_id):
    if request.method == 'GET':
        userdata = db.session.query(Users).filter_by(id=user_id).first()
        data={
            'id':userdata.id,
            'username':userdata.username,
            'name':userdata.name,
            'photo':"/uploads/"+userdata.photo,
            'email':userdata.email,
            'location':userdata.location,
            'biography':userdata.biography,
            'date_joined':(userdata.date_joined).strftime("%B %d, %Y"),
        }
        return jsonify(data=data)
    return  jsonify({'errors': 'Method Not Allowed'})



@app.route('/api/auth/login', methods=['POST'])
def login():
    loginform = LoginForm()

    if loginform.validate_on_submit() and request.method=="POST":
        username=loginform.username.data
        password=loginform.password.data
        user=Users.query.filter_by(username=username).first()
        if user is not None and check_password_hash(user.password, password):
            login_user(user)
            payload = {
                "username": user.username,
                "user":user.name,
                'iat': datetime.datetime.now(datetime.timezone.utc),
                'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)
            }
            encoded_jwt = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
            message = {
                "message": "Login Successful",
                "token": encoded_jwt,
                "id":user.id
            }

            return jsonify(message=message)

        else:
            errors = {
            "errors": ["Username or Password is incorrect."]
            }
            return jsonify(errors=errors)
    else:
        errors = {
            "errors": form_errors(loginform)
        }
        return jsonify(errors=errors)



@app.route('/api/auth/logout', methods=['GET'])
def logout():
    logout_user()
    message = {
    "message": "Log out successful"
    }
    return jsonify(message=message)
# Please create all new routes and view functions above this route.
# This route is now our catch all route for our VueJS single page
# application.
@app.route('/')
def index():
    return send_file(os.path.join('../dist/', 'index.html'))

# Here we define a function to collect form errors from Flask-WTF
# which we can later use

@app.route('/uploads/<filename>')
def get_image(filename):
    rootdir = os.getcwd()
    return send_from_directory(os.path.join(rootdir,app.config['UPLOAD_FOLDER']),filename)

def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages


###
# The functions below should be applicable to all Flask apps.
###
@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
