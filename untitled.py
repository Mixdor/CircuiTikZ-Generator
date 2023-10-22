import re

expresion_regular = r'^\[[a-zA-Z0-9\s]+\]$'

# Ejemplo de uso
cadena = "[Battery 1]"
if re.match(expresion_regular, cadena):
    print("La cadena es válida.")
else:
    print("La cadena no es válida.")