from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


# User Model

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    major = db.Column(db.String(100), nullable=False)

    role = db.Column(db.String(20), default='user')   # user / admin
    paid = db.Column(db.Boolean, default=False)       # حالة الدفع

    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



# Opportunity Model

class Opportunity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    field = db.Column(db.String(100), nullable=False)  # مجال الدورة

# تسجيل الفرص للمستخدمين
class OpportunityRegistration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    major = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunity.id'))  # 👈 اختياري لو بدك تربطي التسجيل بالدورة

    opportunity = db.relationship('Opportunity', backref='registrations')

class OpportunityRegistration(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    major = db.Column(db.String(100))
    phone = db.Column(db.String(20))

    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunity.id'))