from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class CafeRating(db.Model):
    __tablename__= "cafe_ratings"

    id = db.Column(db.Integer, primary_key=True)
    cafe_name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(80), nullable=False)
    open_time = db.Column(db.String(120), nullable=False)
    close_time = db.Column(db.String(120), nullable=False)
    coffee_rating = db.Column(db.String(120), nullable=False)
    wifi_rating = db.Column(db.String(120), nullable=False)
    socket_rating = db.Column(db.String(120), nullable=False)
    
    def __repr__(self):
        return '<Cafe Rating of: %r>' % self.cafe_name