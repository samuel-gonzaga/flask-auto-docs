# forms.py (deve estar no mesmo diretório)
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, DecimalField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from datetime import datetime

class DocumentForm(FlaskForm):
    nome_cliente = StringField('Nome Completo', validators=[
        DataRequired(),
        Length(min=5, max=100)
    ])
    cpf = StringField('CPF', validators=[
        DataRequired(),
        Length(min=11, max=14)
    ])
    rg = StringField('RG', validators=[DataRequired()])
    data_contrato = DateField('Data do Contrato', format='%d/%m/%Y', default=datetime.now)
    valor = DecimalField('Valor', places=2, validators=[DataRequired()])
    observacoes = TextAreaField('Observações')
    submit = SubmitField('Gerar Documento')