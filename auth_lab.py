from flask import Flask, request, render_template_string, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
# Clave aleatoria para proteger las cookies de sesión local
app.secret_key = os.urandom(24)

# Base de datos simulada en memoria
USERS_DB = {
    "admin@example.com": {
        "username": "AdminLab",
        "password": generate_password_hash("Seguridad2026!") # Contraseña protegida con Hash
    }
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Laboratorio de Autenticación Segura</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f4f4f9; text-align: center; margin-top: 50px; }
        .card { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); display: inline-block; width: 300px; }
        input { width: 90%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 4px; }
        button { width: 96%; padding: 10px; background: #007BFF; color: white; border: none; border-radius: 4px; cursor: pointer; }
        .msg { color: red; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="card">
        <h2>{{ title }}</h2>
        {% if msg %}<p class="msg">{{ msg }}</p>{% endif %}
        
        {% if not logged_in %}
        <form method="POST" action="/login">
            <input type="email" name="email" placeholder="Correo electrónico" required><br>
            <input type="password" name="password" placeholder="Contraseña" required><br>
            <button type="submit">Iniciar Sesión</button>
        </form>
        {% else %}
            <p>Bienvenido, <strong>{{ session['username'] }}</strong></p>
            <p>Estado de la cuenta: <span style="color: green;">Verificada</span></p>
            <a href="/logout"><button style="background: #DC3545;">Cerrar Sesión</button></a>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    if 'email' in session:
        return render_template_string(HTML_TEMPLATE, title="Panel de Usuario", logged_in=True)
    return render_template_string(HTML_TEMPLATE, title="Acceso al Sistema", logged_in=False, msg=request.args.get('msg', ''))

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    user = USERS_DB.get(email)
    
    # Simulación de control de seguridad básico contra fuerza bruta o accesos inválidos
    if user and check_password_hash(user['password'], password):
        session['email'] = email
        session['username'] = user['username']
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index', msg="Credenciales incorrectas o usuario inexistente"))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index', msg="Sesión cerrada correctamente"))

if __name__ == '__main__':
    # Ejecución local en el puerto 5001 para no chocar con tu otra app
    app.run(port=5001)
