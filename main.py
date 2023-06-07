from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from flask import request,jsonify

app= Flask(__name__)

basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db= SQLAlchemy(app)
ma= Marshmallow(app)



class User(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    name =db.Column(db.String(100))
    contact = db.Column(db.String(100),unique=True)
    
    def __init__(self,name,contact):
        self.name=name
        self.contact=contact
        
        
class Userschema(ma.Schema):
    class Meta:
        fields=('id','name','contact')


user_schema=Userschema()
users_schema=Userschema(many=True)

with app.app_context():
    db.create_all()
    
#Add New User
@app.route('/user',methods=['POST'])
def add_user():
    name=request.json['name']
    contact=request.json['contact']
    new_user=User(name=name,contact=contact)
    db.session.add(new_user)
    db.session.commit()
    return  user_schema.jsonify(new_user)
#Show users
@app.route('/user',methods=['GET'])
def all_userUsers():
    all_users=User.query.all()
    result=users_schema.dump(all_users)
    return jsonify(result)
if __name__ == '__main__':
    app.run(debug=True,port=5000)
    db.create_all()
