import flask
from flask import Flask, jsonify, render_template, request,flash,url_for
import random
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from werkzeug.utils import redirect

'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new_cafes.db'
app.secret_key="fnihiuqv4nviuhviuq"
SECRET_CODE="dhqihvnvq4hv4qnvnvuv985u93ur149872cjk4bu"
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class New_Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean,nullable=True)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean,nullable=True)
    can_take_calls: Mapped[bool] = mapped_column(Boolean,nullable=True)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)




with app.app_context():
    db.create_all()


@app.route("/")
def home():
    all_cafes=New_Cafe.query.all()

    return render_template("index.html",cafes=all_cafes)


@app.route("/all",methods=["GET","POST"])
def fetch_all():
    cafes=db.session.execute(db.select(New_Cafe).order_by(New_Cafe.name))
    all_cafes=cafes.scalars().all()
    list_of_cafes={"cafes":[]}
    for cafes in all_cafes:
        cafees={
        'location': cafes.location,
        'name': cafes.name,

        'amenties': {
            "seats": cafes.seats,
            "has_toilet": cafes.has_toilet,
            "has_wifi": cafes.has_wifi,
            "has_sockets": cafes.has_sockets,
            "can_take_calls": cafes.can_take_calls,
            "coffee_price": cafes.coffee_price,
        }
        }
        list_of_cafes["cafes"].append(cafees)





    return jsonify(list_of_cafes)




@app.route("/search",methods=["GET","POST"])

def search():
    loc = request.args.get("loc")
    requested_cafe=db.session.execute(db.select(New_Cafe).filter_by(location=loc)).scalars().all()
    if requested_cafe:
        return jsonify(cafes=[{
            "location":cafe.location,
            "name":cafe.name,
        } for cafe in requested_cafe])
    else:
        return jsonify(error={"not found": "khel khtm data khtm"})








# HTTP GET - Read Record

# HTTP POST - Create Record
@app.route("/add",methods=["GET","POST"])
def add():

    if request.method=="POST":
        new_cafe=New_Cafe(name=request.form['cafe_name'],
                      location=request.form['location'],
                      seats=request.form['seats'],
                      has_wifi=request.form['has_wifi']=="on",
                      coffee_price=request.form['coffee_price'],
                      map_url=request.form['map_url'],
                      img_url=request.form['images'])
        existing_cafe=db.session.execute(db.select(New_Cafe).where(New_Cafe.name==request.form["cafe_name"])).scalar_one_or_none()
        if existing_cafe:
            flash("Already exists")
        else:
            db.session.add(new_cafe)
            db.session.commit()
            flash("Input added")
            return redirect(url_for('home'))

    return render_template('add.html')



# HTTP PUT/PATCH - Update Record

@app.route("/edit/<int:id>",methods=['GET','POST'])
def edit_cafe(id):
    all_cafes=db.session.execute(db.select(New_Cafe).filter_by(id=id)).scalar_one_or_none()

    if request.method=="POST":


        all_cafes.name=request.form['new_cafe_name']
        all_cafes.location=request.form['new_location']
        all_cafes.seats=request.form['new_seats']
        all_cafes.has_wifi=request.form['new_has_wifi']=="on"
        all_cafes.coffee_price=request.form['new_coffee_price']
        all_cafes.map_url=request.form['new_map_url']
        all_cafes.img_url=request.form['new_img_url']
        all_cafes.has_toilet=request.form['new_has_toilet']=="on"

        db.session.commit()
        flash("successfully updated")
        return redirect(url_for('home'))





    return render_template("edit_cafe.html",cafe=all_cafes)


# HTTP DELETE - Delete Record

@app.route('/delete/<int:id>',methods=['GET','POST'])
def Delete_Cafe(id):
    cafe=db.session.execute(db.select(New_Cafe).where(New_Cafe.id==id)).scalar_one_or_none()
    if request.method=="POST":
        if request.form['secret_code']==SECRET_CODE:
            to_delete=db.session.execute(db.select(New_Cafe).where(New_Cafe.id==id)).scalar_one_or_none()
            if to_delete:
                db.session.delete(to_delete)
                db.session.commit()
                flash("Cafe deletion succesful")
            return redirect(url_for('home'))
        else:
            return """<h1> Acha bete Bakchodi shi hai kr kr </h1>"""
    return render_template('delete_cafe.html',cafe=cafe)




if __name__ == '__main__':
    app.run(debug=True)
