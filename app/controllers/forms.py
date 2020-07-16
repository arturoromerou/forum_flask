from wtforms import Form
from wtforms import StringField, PasswordField
from wtforms import validators

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