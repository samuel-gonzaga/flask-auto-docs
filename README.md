# 📄 Gerador de Documentos Automatizado

**Sistema para geração automatizada de documentos jurídicos e contratos a partir de templates Word (.docx)**

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1-lightgrey.svg)](https://flask.palletsprojects.com/)

## ✨ Funcionalidades

- **Upload de templates** em formato DOCX ou TXT
- **Reconhecimento automático** de campos (ex: `{{nome_cliente}}`)
- **Geração de formulários** dinâmicos com validação
- **Preenchimento inteligente** com máscaras para:
  - CPF/CNPJ
  - Datas
  - Valores monetários
  - Telefones
- **Download automático** dos documentos gerados
- **Interface intuitiva** com confirmações de segurança

## 🛠️ Tecnologias

- Python 3.12+
- Flask (Web Framework)
- python-docx (Processamento de Word)
- Flask-WTF (Formulários seguros)
- Bootstrap 5 (Interface)
- Jinja2 (Templates HTML)

## 🚀 Como Executar

### Pré-requisitos
```bash
python -m venv venv
venv\Scripts\activate     # Windows
```

## Instalação

```
pip install -r requirements.txt
```

## Configuração
Crie um arquivo .env na raiz:
```
SECRET_KEY=sua_chave_secreta_aqui
```

## Execução
```
python main.py
```
Acesse: http://localhost:5000

## 📂 Estrutura de Arquivos

```
/
├── blueprints/              # Rotas do sistema
├── generated/               # Arquivos gerados
├── logs/                    # logs do sistema
├── services/                # Lógica de processamento
├── static/                  # CSS/JS
├── templates/               # Templates HTML
├── .env                     # Variaveis de ambiente
├── .gitignore               # .gitignore de arquivos
└── config.py                # Configurações
└── forms.py                 # Configurações de formulários
└── logger_config.py         # Configurações de logs
└── main.py                  # Ponto de entrada
└── README.md                # Este arquivo
├── requirements.txt         # Dependências
```

## 🛡️ Segurança

- Proteção CSRF em todos os formulários
- Validação rigorosa de caminhos de arquivos
- Sanitização de nomes de arquivos
- Logging detalhado de operações

📝 Como Usar
- Acesse /upload para enviar um template
- Use placeholders no formato {{campo}}
- O sistema criará um formulário automático
- Preencha os dados e gere o documento

## 📌 Exemplo de Template

```
Pelo presente instrumento, {{nome_cliente}}, 
portador do CPF {{CPF}}, concorda com os termos 
em {{data_contrato}} no valor de R$ {{valor}}.
```

## 🤝 Contribuição

1. Contribuições são bem-vindas! Siga os passos:
2. Fork este repositório
3. Crie um branch (git checkout -b feature/nova-funcionalidade)
4. Commit suas mudanças (git commit -m 'Adiciona nova funcionalidade')
5. Push para o branch (git push origin feature/nova-funcionalidade)
6. Abra um Pull Request

