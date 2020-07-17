from wtforms import Form
from wtforms import StringField, PasswordField, TextField, DateField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms import HiddenField
from wtforms import validators
from app.models.model import User

def length_honeypot(form, field):
    if len(field.data) > 0:
        raise validators.ValidationError('el campo debe estar vacio')

class CreateForm(Form):
    username = StringField('Username',
                        [ 
                            validators.Required(message='el username es requerido'),
                            validators.length(min=4, max=25, message='ingresa un username valido!.')
                        ]
                        )

    password = PasswordField('Password', 
                            [
                                validators.Required(message='El password es requerido')
                            ]
                            )

    email = EmailField('Correo Electronico',
                    [
                        validators.Required(message='el email es requerido'),
                        validators.Email(message='ingresa un email valido'),
                        validators.length(min=4, max=50, message='ingrese un email valido')
                    ]
                    )

    honeypot = HiddenField('', [length_honeypot])

    def validate_username(form, field):
        username = field.data
        user = User.query.filter_by(username = username).first()
        if user is not None:
            raise validators.ValidationError('el username ya existe! :(')

class LoginForm(Form):
    
    username = StringField('Usuario',
                        [ 
                            validators.Required(message='el username es requerido'),
                            validators.length(min=4, max=25, message='ingresa un username valido!.')
                        ]
                        )
    password = PasswordField('Contraseña', 
                            [
                                validators.Required(message='El password es requerido')
                            ]
                            )

class CommentForm(Form):
    
    comment = TextAreaField('Comentario')
    honeypot = HiddenField('', [length_honeypot])

