from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError,Email
from models import User


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=4, max=20)]
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8),
            EqualTo("confirm_password", message=" Both password must match! "),
        ],
    )
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already exists.")


class MemberForm(FlaskForm):
    banner_id = StringField('Banner ID', validators=[DataRequired()])
    tiger_email = StringField('Tiger Email', validators=[DataRequired(),Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone = StringField('Phone',validators=[DataRequired()])
    personal_email = StringField('Personal Email',validators=[DataRequired(),Email()])
    current_city = StringField('Current City',validators=[DataRequired()])
    current_employer = StringField('Current Employer',validators=[DataRequired()])
    graduation_date = StringField('Graduation Date',validators=[DataRequired()])
    linkedin = StringField('LinkedIn',validators=[DataRequired()])
    graduating_employer = StringField('Graduating Employer',validators=[DataRequired()])
    internship1 = StringField('Internship 1',validators=[DataRequired()])
    internship2 = StringField('Internship 2',validators=[DataRequired()])
    internship3 = StringField('Internship 3',validators=[DataRequired()])
    additional_degrees = StringField('Additional Degrees',validators=[DataRequired()])
    address = StringField('Address',validators=[DataRequired()])
    submit = SubmitField('Submit')
