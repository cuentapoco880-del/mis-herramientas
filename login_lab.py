#!/usr/bin/env python3
from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Configuración inicial de la base de datos en memoria
def iniciar_base_de_datos():
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    cursor = conn.cursor()
    # Crear tabla de usuarios
    cursor.execute("""
        CREATE TABLE usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT,
            contrasena TEXT,
            rol TEXT
        )
    """)
    # Insertar un usuario administrador de prueba
    cursor.execute("INSERT INTO usuarios (usuario, contrasena, rol) VALUES ('admin', 'SuperClave2026', 'Administrador')")
    cursor.execute("INSERT INTO usuarios (usuario, contrasena, rol) VALUES ('brian', 'invitado123', 'Usuario')")
    conn.commit()
    return conn

db_conn = iniciar_base_de_datos()

# Interfaz visual del Login (HTML básico integrado)
LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Laboratorio de Autenticacion</title>
    <style>
        body { font-family: Arial; background: #1a1a1a; color: white; text-align: center; padding-top: 50px; }
        .box { background: #2a2a2a; padding: 20px; display: inline-block; border-radius: 8px; }
        input { display: block; margin: 10px auto; padding: 10px; width: 200px; }
        button { padding: 10px 20px; background: #00cc66; border: none; color: white; cursor: pointer; }
    </style>
</head>
<body>
    <div class="box">
        <h2>CyberOS Login Lab</h2>
        <form method="POST" action="/login">
            <input type="text" name="user" placeholder="Usuario" required>
            <input type="password" name="password" placeholder="Contrasena" required>
            <button type="submit">Ingresar</button>
        </form>
        <p style="color: gray;">{{ mensaje }}</p>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(LOGIN_HTML, mensaje="Introduce credenciales")

@app.route('/login', methods=['POST'])
def login():
    user = request.form.get('user')
    password = request.form.get('password')
    
    cursor = db_conn.cursor()
    
    # ¡AQUÍ ESTÁ LA VULNERABILIDAD!
    # Al concatenar las variables directamente con '{}', el sistema ejecutará cualquier código que metas ahí.
    query = "SELECT * FROM usuarios WHERE usuario = '{}' AND contrasena = '{}'".format(user, password)
    print(f"\n[!] Consulta SQL ejecutada en el servidor:\n{query}\n")
    
    try:
        cursor.execute(query)
        resultado = cursor.fetchone()
        
        if resultado:
            return render_template_string(LOGIN_HTML, mensaje=f"✓ Acceso Concedido. Bienvenido: {resultado[1]} (Rol: {resultado[3]})")
        else:
            return render_template_string(LOGIN_HTML, mensaje="X Credenciales incorrectas.")
    except Exception as e:
        return render_template_string(LOGIN_HTML, mensaje=f"[-] Error en la base de datos: {e}")

if __name__ == '__main__':
    # Escucha en el puerto 5000 de tu red local
    app.run(host='0.0.0.0', port=5000, debug=True)
