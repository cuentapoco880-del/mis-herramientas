import sqlite3
from flask import Flask, request, render_template_string

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INT, username TEXT, role TEXT)")
    cursor.execute("INSERT INTO users VALUES (1, 'admin', 'SuperAdministrador')")
    cursor.execute("INSERT INTO users VALUES (2, 'brian', 'Developer')")
    conn.commit()
    return conn

db_conn = init_db()

@app.route('/')
def index():
    user_id = request.args.get('id', '')
    if not user_id:
        return "<h3>Buscador de usuarios de prueba. Usa: /?id=1</h3>"
    
    cursor = db_conn.cursor()
    try:
        # Vulnerabilidad de Inyección SQL por concatenación directa
        query = f"SELECT username, role FROM users WHERE id = {user_id}"
        cursor.execute(query)
        resultado = cursor.fetchall()
        
        if resultado:
            return render_template_string(f"<h4>Resultado de la consulta:</h4><p>{str(resultado)}</p>")
        else:
            return "<h4>Usuario no encontrado.</h4>"
    except Exception as e:
        return f"<h4>Error en el servidor:</h4><code>{str(e)}</code>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
