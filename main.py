from flask import Flask, render_template, url_for, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
import csv
# import sqlite3
from models import CafeRating, db


### this used sqlite to create the database, replaced with SQLAlchemy
# creates db
# db = sqlite3.connect('cafe-ratings.db', timeout=10)
# cursor = db.cursor()
# cursor.execute("CREATE TABLE cafes (" \
#                     "name varchar(50) NOT NULL UNIQUE," \
#                         "location varchar(250) NOT NULL UNIQUE," \
#                             "openTime STRING NOT NULL," \
#                             "closeTime STRING NOT NULL," \
#                             "coffeeRating FLOAT NOT NULL," \
#                             "wifiRating FLOAT NOT NULL," \
#                             "socketRating FLOAT NOT NULL)")

# cursor.execute("INSERT INTO cafes VALUES('caasdfe', 'locaasdf', '6:00am', '6:00pm', '☕☕', '💪💪💪💪','🔌🔌🔌🔌')")
# db.commit()
### end of sqlite 


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db.app = app
db.init_app(app)
#db.create_all()

#CafeRating(cafe_name="cname",location="location link",open_time="1:00am",close_time="1:00pm",coffee_rating="☕",wifi_rating='💪💪',socket_rating='🔌🔌🔌')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('location', validators=[DataRequired()])
    open = StringField('open-time', validators=[DataRequired()])
    close = StringField('close-time', validators=[DataRequired()])
    coffee = SelectField('coffee-rating', validators=[DataRequired()],choices=['☕','☕☕','☕☕☕','☕☕☕☕','☕☕☕☕☕'])
    wifi = SelectField('wifi-rating', validators=[DataRequired()],choices=['💪','💪💪','💪💪💪','💪💪💪💪','💪💪💪💪💪'])
    socket = SelectField('socket-availability', validators=[DataRequired()], choices=['🔌','🔌🔌','🔌🔌🔌','🔌🔌🔌🔌','🔌🔌🔌🔌🔌'])
    submit = SubmitField('Submit')


# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("true")
        
        ### old code used to add/store data in csv
        # row_data = []
        # row_data.append(form.cafe.data)
        # row_data.append(form.location.data)
        # row_data.append(form.open.data)
        # row_data.append(form.close.data)
        # row_data.append(form.coffee.data)
        # row_data.append(form.wifi.data)
        # with open('62_bootstrapflask_WTForms/static/cafe-data.csv', 'a') as csv_file:
        #     csv_file.write('\n')
        #     for column in row_data:
        #         csv_file.write(column + ", ")
        #     csv_file.write(form.socket.data)
        ### end of old code

        ### add to database instead of csv
        # read form data and add to db table
        new_rating = CafeRating(cafe_name=form.cafe.data,
                                location=form.location.data,
                                open_time=form.open.data,
                                close_time=form.close.data,
                                coffee_rating=form.coffee.data,
                                wifi_rating=form.wifi.data,
                                socket_rating=form.socket.data)
        db.session.add(new_rating)
        db.session.commit()

        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    ### old code to read data from csv
    # with open('62_bootstrapflask_WTForms/static/cafe-data.csv', newline='') as csv_file:
    #     csv_data = csv.reader(csv_file, delimiter=',')
    #     list_of_rows = []
    #     for row in csv_data:
    #         list_of_rows.append(row)
    ### end of old code

    ### read data from database instead of csv
    all_ratings = db.session.query(CafeRating).all()
    print(all_ratings)
    print(all_ratings)
    return render_template('cafes.html', cafes=all_ratings)


if __name__ == '__main__':
    app.run(debug=True)
