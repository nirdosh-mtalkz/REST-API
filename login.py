from flask import Flask,request
import requests
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db=SQLAlchemy(app)

class Emp(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20),unique=True,nullable=False)
    password = db.Column(db.String(20))

    def __repr__(self):
        return f"{self.name} - {self.password}"

@app.route('/')
def home():
    return {"name":"password"}

@app.route('/login')
def show():
    emp = Emp.query.all()
    output=[]
    for e in emp:
        tmp = {'id':e.id,'name':e.name,'password':e.password}
        output.append(tmp)
    return {"Employee":output}

@app.route('/login/<int:id>')
def d_byid(id):
    #emp=Emp.query.all()
    emp=Emp.query.get_or_404(id)
    '''for e in emp:
        if id==e.id:
            tmp = {'id':e.id,'name':e.name,'password':e.password}
            return {"Employee":tmp}
    return "Not Found"
    '''
    return {'id':emp.id,'name':emp.name,'password':emp.password}

@app.route('/add-emp',methods=['POST'])
def add():
    emp = Emp(id=request.json['id'],name=request.json['name'],password=request.json['password'])
    db.session.add(emp)
    db.session.commit()
    return "Successfully added %s"%emp.name

@app.route('/dlt-emp/<id>',methods=['DELETE'])
def dlt(id):
    emp=Emp.query.get(id)
    if emp is None:
        return {"not found":"404"}
    db.session.delete(emp)
    db.session.commit()
    return {"delted id":emp.id}


if __name__ == "__main__":
    app.run(debug=True)