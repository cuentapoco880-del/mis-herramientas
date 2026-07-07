import zipfile
import itertools
import string
import sys
import time

print("--- RECOBRADOR DE CONTRASEÑAS POR FUERZA BRUTA ---")
archivo_zip = "secreto.zip"  # El archivo que está en tu escritorio

# Definimos los caracteres que va a probar (letras minúsculas y números)
# Puedes agregar string.ascii_uppercase si usaste mayúsculas
caracteres = string.ascii_lowercase + string.digits

try:
    with zipfile.ZipFile(archivo_zip) as archivo:
        print(f"[*] Analizando archivo: {archivo_zip}")
        print("[*] Probando combinaciones (esto puede tardar según la longitud)...")
        
        inicio = time.time()
        
        # El script probará longitudes de contraseña desde 1 hasta 6 caracteres
        for longitud in range(1, 7):
            print(f"\n[+] Probando contraseñas de longitud: {longitud}")
            
            # Genera todas las combinaciones posibles matemáticamente
            for combinacion in itertools.product(caracteres, repeat=longitud):
                # Une los caracteres para formar la contraseña en texto
                intento = "".join(combinacion)
                
                try:
                    # Intenta extraer el archivo usando la contraseña (en formato bytes)
                    archivo.extractall(pwd=intento.encode('utf-8'))
                    
                    # Si no da error, ¡la contraseña es correcta!
                    tiempo_total = round(time.time() - inicio, 2)
                    print("\n==============================================")
                    print(f"¡ÉXITO! Contraseña encontrada: {intento}")
                    print(f"Tiempo transcurrido: {tiempo_total} segundos.")
                    print("==============================================")
                    sys.exit(0)
                except (zipfile.BadZipFile, RuntimeError, PermissionError):
                    # Si da error de contraseña incorrecta, continúa con la siguiente
                    continue

        print("\n[-] No se encontró la contraseña en el rango de 1 a 6 caracteres.")

except FileNotFoundError:
    print(f"❌ Error: No se encontró el archivo '{archivo_zip}' en esta carpeta.")
