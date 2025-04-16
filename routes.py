from main import app
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, InputRequired, EqualTo, Email

class RegisterForm(FlaskForm):
    first_name = StringField('Primeiro nome', validators=[DataRequired()])
    last_name = StringField('Sobrenome')
    email = EmailField('email', validators=[Email(message="E-Mail Inválido!")])
    password = PasswordField('Senha', validators=[InputRequired(), EqualTo('confirm', message="As senhas devem ser identicas")])
    confirm = PasswordField('Confirme a senha', validators=[DataRequired()])
    submit = SubmitField('Cadastrar')

# Rotas
@app.route('/', methods=["GET", "POST"])
def root():
    form = RegisterForm()

    form.validate_on_submit()
    return render_template("homepage.html", form=form)

@app.route('/blog')
def blog():
    return "Bem vindo ao blog" 