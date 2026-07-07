#!/bin/bash
# Script para subir desarrollos automáticamente desde Android

# Añadir todos los archivos nuevos o modificados al paquete
git add .

# Hacer el commit con la fecha y hora actual
git commit -m "Update desde Termux: $(date +'%Y-%m-%d %H:%M:%S')"

# Subir los cambios a GitHub
git push origin main

echo "[✓] Todo se subió correctamente a la cuenta cuentapoco880-del."
