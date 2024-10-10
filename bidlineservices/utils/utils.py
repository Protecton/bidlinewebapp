import re

def concatenar_valores(template, valores):
    # Usamos regex para buscar patrones como $1, $2, etc.
    def replace_match(match):
        index = int(match.group(1)) - 1  # Extraemos el número del placeholder ($1 -> index = 0)
        if 0 <= index < len(valores):
            return str(valores[index])
        return match.group(0)  # Si no se encuentra un valor adecuado, devolvemos el placeholder original

    # Reemplazamos todos los $n con sus respectivos valores
    return re.sub(r'\$\$\$(\d+)', replace_match, template)

# # Ejemplo de uso
# resultado = concatenar_valores("Hola $1, estoy en $2 horas", ["Gustavo", 20])
# print(resultado)  # Salida: "Hola Gustavo, estoy en 20 horas"

# cadena = concatenar_valores("Hola $$$1, estoy a $$$2 horas", ["Robert", 10])
# return JsonResponse({"message": cadena}, safe=False)