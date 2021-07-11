from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, ValidationError


class Validator:
    @staticmethod
    def check_name(form, field):
        data = field.data.strip()
        if data.isspace():
            raise ValidationError("Name contains space")
        elif not data.isalpha():
            raise ValidationError("Name contains invalid characters")


class RegistrationForm(FlaskForm):
    # firstname = StringField('Firstname', validators=[DataRequired(),
    #             Length(min=3, max=15)] , render_kw={"placeholder": "First Name"})

    # In the StringField 'Firstname' is the tag name which will be displayed on the web page
    #
    # firstname = StringField('Firstname', validators=[DataRequired(),
    #                                                  Length(min=3, max=15), Validator.check_name],
    #                         render_kw={"placeholder": "First Name"})
    # lastname = StringField('Lastname', validators=[DataRequired(),
    #                                                Length(min=3, max=20), Validator.check_name],
    #                        render_kw={"placeholder": "Last Name"})

    firstname = StringField('Firstname', validators=[DataRequired(), Length(min=3, max=15), Validator.check_name],
                            render_kw={"placeholder": "First Name"})
    lastname = StringField('Lastname', validators=[DataRequired(), Length(min=3, max=15), Validator.check_name],
                           render_kw={"placeholder": "Last Name"})

    email = StringField('Email ', validators=[DataRequired(), Email() , Length(min=10, max=30)],
                        render_kw={"placeholder": "Email"})
    password = PasswordField('Password ', validators=[DataRequired(),
                                                      Length(min=8, max=12)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Length(min=10, max=25), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=12)],
                             render_kw={"placeholder": "Password"})
    choices = ['Citizen', 'Councillor']
    choice = SelectField('Role :', choices=choices, validators=[DataRequired()])
    submit = SubmitField('Login')
