from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin,
    login_user, logout_user,
    login_required, current_user
)
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

from forms import RegisterForm, LoginForm, OpportunityForm

# ======================
# إعداد التطبيق
# ======================
app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blueacademy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ======================
# موديل المستخدم
# ======================
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    major = db.Column(db.String(150), nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    cv_file = db.Column(db.String(200))
    role = db.Column(db.String(20), default="user")
    paid = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# ======================
# موديل تسجيل الفرص
# ======================
class OpportunityRegistration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    major = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ======================
# الصفحات
# ======================
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('هذا البريد مسجل مسبقًا')
            return redirect(url_for('register'))

        major = form.other_major.data if form.other_major.data else form.major.data

        file = form.cv.data
        filename = secure_filename(file.filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        user = User(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            major=major,
            cv_file=filename
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash('تم إنشاء الحساب بنجاح')
        return redirect(url_for('home'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('تم تسجيل الدخول')
            if user.role == 'admin':
                return redirect(url_for('admin'))
            return redirect(url_for('home'))
        flash('بيانات الدخول غير صحيحة')

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('تم تسجيل الخروج')
    return redirect(url_for('home'))

@app.route('/team')
def team():
    return render_template('team.html')

# ======================
# راوت الاشتراك بالفرص
# ======================
@app.route('/opportunity-register', methods=['GET', 'POST'])
def opportunity_register():
    form = OpportunityForm()

    if form.validate_on_submit():
        registration = OpportunityRegistration(
            name=form.name.data,
            major=form.major.data,
            phone=form.phone.data
        )

        db.session.add(registration)
        db.session.commit()

        flash('تم استلام طلبك بنجاح ✅')
        return redirect(url_for('home'))

    return render_template('opportunity_register.html', form=form)

@app.route('/opportunities')
def opportunities():
    return render_template('opportunities.html')

# ======================
# لوحة الأدمن
# ======================
@app.route('/admin')
@login_required
def admin():
    if current_user.role != 'admin':
        abort(403)

    users = User.query.all()
    registrations = OpportunityRegistration.query.all()
    return render_template('admin.html', users=users, registrations=registrations)

# ======================
# تبديل حالة الدفع
# ======================
@app.route('/toggle-paid/<int:user_id>', methods=['POST'])
@login_required
def toggle_paid(user_id):
    if current_user.role != 'admin':
        abort(403)

    user = User.query.get_or_404(user_id)
    if user.role == 'admin':
        flash("لا يمكنك تعديل حالة الأدمن")
        return redirect(url_for('admin'))

    user.paid = not user.paid
    db.session.commit()

    flash(f"تم تحديث حالة الدفع للمستخدم {user.name}")
    return redirect(url_for('admin'))

# ======================
# إنشاء أدمن
# ======================
@app.route('/create-admin')
def create_admin():
    admin_email = "admin@blue.com"
    admin_password = "12345678"

    admin = User.query.filter_by(email=admin_email).first()
    if admin:
        return "الأدمن موجود مسبقًا !!"

    admin = User(
        name="Admin",
        email=admin_email,
        phone="0000000000",
        major="Administration",
        role="admin"
    )
    admin.set_password(admin_password)
    db.session.add(admin)
    db.session.commit()

    return "تم إنشاء حساب الأدمن بنجاح ✅"

# ======================
# تشغيل التطبيق
# ======================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


