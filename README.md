# API-mobile

## 1. Requisitos
Antes de iniciar, tenha instalado:

- Python 3.10+  
- pip  
- Virtualenv

## 2. Criar e ativar o ambiente virtual

Windows
python -m venv venv
venv\Scripts\activate

Linux
python3 -m venv venv
source venv/bin/activate

## 3. Instalar dependências
pip install -r requirements.txt

## 4. Aplicar migrações
python manage.py migrate

## 5. Criar superusuário
python manage.py createsuperuser

Siga as instruções no terminal para criar o usuário.

## 6. Executar o servidor
python manage.py runserver

O backend ficará disponível em:
http://127.0.0.1:8000/

## 7. Acessar o AdminPanel customizado
URL:
http://127.0.0.1:8000/panel/login/