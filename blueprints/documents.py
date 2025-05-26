from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file
from datetime import datetime
from werkzeug.utils import secure_filename
from services.document_processor import DocumentProcessor
from config import Config
import os
from forms import DocumentForm

bp = Blueprint('documents', __name__)
doc_processor = DocumentProcessor(Config.UPLOAD_FOLDER, Config.GENERATED_FOLDER)


@bp.route('/')
def index():
    templates = doc_processor.get_available_templates()
    return render_template('index.html', templates=templates)

@bp.route('/form/<template_name>')
def form(template_name):
    form = DocumentForm()

    templates = doc_processor.get_available_templates()
    template = next((t for t in templates if t['filename'] == template_name), None)
    
    if not template:
        flash('Template não encontrado!', 'error')
        return redirect(url_for('documents.index'))
    
    dynamic_fields = []
    for placeholder in template['placeholders']:
        field = {
            'name': placeholder,
            'label': placeholder.replace('_', ' ').title(),
            'type': 'text',
            'required': True
        }
        
        if 'DATA' in placeholder.upper():
            field.update({'type': 'date', 'value': datetime.now().strftime('%Y-%m-%d')})
        elif 'EMAIL' in placeholder.upper():
            field['type'] = 'email'
        
        dynamic_fields.append(field)
    
    return render_template('form.html', 
                         template=template, 
                         fields=dynamic_fields,
                         placeholders_count=len(template['placeholders']))

@bp.route('/upload', methods=['GET', 'POST'])
def upload_template():
    """Rota para upload de novos templates"""
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Nenhum arquivo selecionado!', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('Nenhum arquivo selecionado!', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(Config.UPLOAD_FOLDER, filename))
            flash(f'Template {filename} enviado com sucesso!', 'success')
            return redirect(url_for('documents.index'))
        else:
            flash('Tipo de arquivo não permitido!', 'error')
    
    return render_template('upload.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@bp.route('/generate', methods=['POST'])
def generate_document():
    """Gera o documento preenchido"""
    try:
        template_name = request.form.get('template_name')
        output_name = request.form.get('output_name', f'documento_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
        
        output_name = secure_filename(output_name)
        
        form_data = {}
        for key, value in request.form.items():
            if key not in ['template_name', 'output_name']:
                form_data[key] = value
        
        output_path = doc_processor.process_document(template_name, form_data, output_name)
        
        flash('Documento gerado com sucesso!', 'success')
        
        return send_file(
            output_path,
            as_attachment=True,
            download_name=os.path.basename(output_path)
        )
        
    except Exception as e:
        flash(f'Erro ao gerar documento: {str(e)}', 'error')
        return redirect(url_for('documents.index'))
    
@bp.route('/delete_template/<filename>', methods=['POST'])
def delete_template(filename):
    """Remove um template com tratamento aprimorado de mensagens"""
    try:
        safe_filename = secure_filename(filename)
        if not safe_filename or safe_filename != filename:
            flash('Nome de arquivo inválido!', 'error')
            return redirect(url_for('documents.index'))

        template_path = os.path.join(Config.UPLOAD_FOLDER, safe_filename)
        upload_dir = os.path.abspath(Config.UPLOAD_FOLDER)

        # Verificação única de caminho
        if not os.path.exists(template_path):
            msg = 'Template não encontrado!'
            flash(msg, 'error')
        elif not os.path.isfile(template_path):
            msg = 'Operação não permitida! (Não é um arquivo)'
            flash(msg, 'error')
        elif not os.path.abspath(template_path).startswith(upload_dir):
            msg = 'Operação não permitida! (Caminho inválido)'
            flash(msg, 'error')
        else:
            try:
                os.remove(template_path)
                # Mensagem única de sucesso
                msg = 'Template removido com sucesso!'
                flash(msg, 'success')  # Única chamada para flash de sucesso
                
            except PermissionError as pe:
                msg = f'Erro de permissão: {str(pe)}'
                flash(msg, 'error')
            except Exception as e:
                msg = f'Erro ao remover template: {str(e)}'
                flash(msg, 'error')
                
    except Exception as e:
        msg = 'Erro interno no servidor'
        flash(msg, 'error')
    
    return redirect(url_for('documents.index'))