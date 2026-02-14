from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo

# -----------------------
# فورم التسجيل
# -----------------------
class RegisterForm(FlaskForm):
    name = StringField('الاسم', validators=[DataRequired()])
    
    email = StringField(
        'البريد الإلكتروني',
        validators=[DataRequired(), Email()]
    )
    
    phone = StringField('رقم الجوال', validators=[DataRequired()])
    
    major = SelectField('التخصص', choices=[
        ('Programming', 'البرمجة'),
        ('Accounting', 'المحاسبة'),
        ('AI', 'الذكاء الاصطناعي'),
        ('Business', 'إدارة الأعمال'),
        ('Translation', 'الترجمة')
    ])
    
    other_major = StringField('تخصص آخر (اختياري)')
    
    password = PasswordField(
        'كلمة المرور',
        validators=[DataRequired(), Length(min=6)]
    )
    
    confirm_password = PasswordField(
        'تأكيد كلمة المرور',
        validators=[DataRequired(), EqualTo('password', message="كلمتا المرور غير متطابقتين")]
    )
    
    cv = FileField('رفع السيرة الذاتية (CV)')
    
    submit = SubmitField('تسجيل')


# -----------------------
# فورم تسجيل الدخول
# -----------------------
class LoginForm(FlaskForm):
    email = StringField(
        'البريد الإلكتروني',
        validators=[DataRequired(), Email()]
    )
    
    password = PasswordField(
        'كلمة المرور',
        validators=[DataRequired()]
    )
    
    submit = SubmitField('تسجيل الدخول')


# -----------------------
# فورم الاشتراك بالفرص
# -----------------------
class OpportunityForm(FlaskForm):
    name = StringField('الاسم', validators=[DataRequired()])
    major = StringField('التخصص', validators=[DataRequired()])
    phone = StringField('رقم الجوال', validators=[DataRequired()])
    submit = SubmitField('اشترك الآن')
