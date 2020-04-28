from flask import Flask, Response,request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
from flask_migrate import Migrate
from bson.objectid import ObjectId
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (jwt_required, create_access_token, get_jwt_identity)
from kanpai import Kanpai
from passlib.apps import custom_app_context as pwd_context
import os


app = Flask(__name__)

app.config['SECRET_KEY'] = 'ThisIsmysecretkeythatyou3cantaccess'


# CONFIGURING DATABASE

app.config['SQLALCHEMY_DATABASE_URI']= "postgresql://postgres:alter@localhost:5432/bookslibrary"

db = SQLAlchemy(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)


class NewUser(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    firstname = db.Column(db.String(50),nullable= False,unique= False)
    lastname = db.Column(db.String(50),nullable= False,unique= False)
    role = db.Column(db.String(50))
    email= db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, email, firstname, lastname, role, password):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.role = role
        self.password = password

@app.route('/signup', methods=['POST'])
def user_signup_new():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_user = NewUser(firstname=data['firstName'], lastname=data['lastName'], email=data['email'], password=data['password'], role=data['roles'])

            db.session.add(new_user)
            db.session.commit()
            return {"message": f"User {new_user.email} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}
#

@app.route('/user/signUp', methods=['POST'])
def user_signup():
    # User requestBody validation
    validation_result = schema.validate(request.json)
    if validation_result.get('success', False) is False:
        return Response(
            response=json.dumps(
                {"Error": validation_result.get("error")
                 }
            ),
            status=400,
            mimetype='application/json'
        )

    try:
        userDetails = request.get_json()
        dbResponse = userSignUp(userDetails)
        if dbResponse == "exists":
            return Response(
                response=json.dumps(
                    {"user": "User already exists with provided email Id"
                     }
                ),
                status=409,
                mimetype='application/json'
            )
        else:
            return Response(
                response=json.dumps(
                    {"user": "User created Successfully"
                     }
                ),
                status=201,
                mimetype='application/json'
            )
    # For catching exception
    except Exception as ex:
        print('*********************')

        print(ex)
        print('********************')


# User SignIn Controller
@app.route('/user/signIn', methods=['POST'])
def user_signIn():
    try:
        userLogInDetails = request.get_json()
        dbResponse = signIn(userLogInDetails)
        if dbResponse.__eq__("Error"):
            return Response(
                response=json.dumps(
                    {"Error": "Failed"
                     }
                ),
                status=400,
                mimetype='application/json'
            )
        else:
            return Response(
                response=json.dumps(
                    {"user": dbResponse
                     }
                ),
                status=201,
                mimetype='application/json'
            )
    # For catching exception
    except Exception as ex:
        print('*********************')

        print(ex)
        print('********************')
def signIn(Object):
    try:
        email = Object['email']
        password = Object['password']
        dbResponse= NewUser.query.filter_by(email= email).first()
        result = ""
        if dbResponse:
            if (password, dbResponse.password):
                try:
                    access_token = create_access_token(identity={
                        'firstName': dbResponse.firstname,
                        'lastName': dbResponse.lastname,
                        'email': dbResponse.email,
                        'roles': dbResponse.role
                    })


                except Exception as ex:
                    print(ex)

                result = access_token
                return result
            else:
                result = "Error"
                return result
        else:
            result = "Error"
            return result
    except Exception as ex:
        print('*********************')

        print(ex)
        print('********************')


def userSignUp(data):
    result = "exists"
    new_user = NewUser(firstname=data['firstName'], lastname=data['lastName'], email=data['email'],
                       password=data['password'], role=data['roles'])
    exist_User= NewUser.query.filter_by(email= new_user.email).first()
    if exist_User== None:
        db.session.add(new_user)
        db.session.commit()
        return new_user.email
    else:
        return result


#############################################################
# Validators ################################################
schema = Kanpai.Object({
    "firstName": Kanpai.String().max(20).trim().required("First Name required"),
    "lastName": Kanpai.String().max(20).trim().required("Last Name required"),
    "email": Kanpai.Email().required("email required"),
    "roles": Kanpai.String().max(5).trim().required("User Role Required"),
    "password": Kanpai.String().max(20).trim().required("pass required")
})
#############################################################

if __name__ == "__main__":
    app.run(debug=True)