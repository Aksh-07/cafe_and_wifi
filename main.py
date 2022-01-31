from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    map_url = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    has_sockets = db.Column(db.Integer, nullable=False)
    has_toilet = db.Column(db.Integer, nullable=False)
    has_wifi = db.Column(db.Integer, nullable=False)
    can_take_calls = db.Column(db.Integer, nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    coffee_price = db.Column(db.Integer, nullable=False)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location_url = StringField("Location Url", validators=[DataRequired(), URL()])
    seats = IntegerField("seats", validators=[DataRequired()])
    can_take_calls = SelectField("Can Take Calls", choices=[0, 1], validators=[DataRequired()])
    coffee_price = IntegerField("Coffee Price", validators=[DataRequired()])
    has_wifi = SelectField("Wifi rating", choices=[0, 1], validators=[DataRequired()])
    has_socket = SelectField("Has Socket", choices=[0, 1], validators=[DataRequired()])
    has_toilet = SelectField("Has Toilets", choices=[0, 1], validators=[DataRequired()])
    img_url = StringField("Img Url", validators=[DataRequired(), URL()])
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            map_url=form.location_url.data,
            name=form.cafe.data,
            img_url=form.img_url.data,
            location=form.location.data,
            has_wifi=form.has_wifi.data,
            has_sockets=form.has_socket.data,
            has_seats=form.seats.data,
            can_take_calls=form.can_take_calls.data,
            coffee_price=form.coffee_price.data,
            toilets=form.has_toilet.data
        )

        db.session.add(new_cafe)
        db.session.commit()

    return render_template('add.html', form=form)


@app.route('/cafes', methods=["GET", "POST"])
def cafes():
    all_cafes = Cafe.query.all()

    return render_template('cafes.html', cafes=all_cafes)


if __name__ == '__main__':
    app.run(debug=True)
