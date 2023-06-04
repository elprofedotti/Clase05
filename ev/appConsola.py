import requests
from googletrans import Translator
import os

base_url = "http://localhost:8080"

endpoints = {
    "1": {
        "endpoint": "/post",
        "fields": ["userId", "id", "title", "body"]
    },
    "2": {
        "endpoint": "/comments",
        "fields": ["postId", "id", "name", "email", "body"]
    },
    "3": {
        "endpoint": "/albums",
        "fields": ["userId", "id", "title"]
    },
    "4": {
        "endpoint": "/photos",
        "fields": ["albumId", "id", "title", "url", "thumbnailUrl"]
    },
    "5": {
        "endpoint": "/todos",
        "fields": ["userId", "id", "title", "completed"]
    },
    "6": {
        "endpoint": "/users",
        "fields": ["id", "name", "username", "email", "address", "phone", "website", "company"]
    }
}

data = {}
    
def limpiar_pantalla():
    if os.name == 'nt':  # para windows
        _ = os.system('cls')
    else:  # para mac y linux
        _ = os.system('clear')
        
def mostrarMenu():
    limpiar_pantalla()
    print("\n--- Menú ---")
    print("1. Ver posts")
    print("2. Ver comentarios")
    print("3. Ver álbumes")
    print("4. Ver fotos")
    print("5. Ver todos")
    print("6. Ver usuarios")
    print("0. Salir")
    
def main():
    while True:
        mostrarMenu()
        opcion = input("Elige una opción: ")
        if opcion == "0":
            break
    
        if opcion in endpoints: #["1", "2", "3", "4", "5", "6"]:
            endpoint = endpoints[opcion]["endpoint"]
            url = base_url + endpoint
            
            response = requests.get(url)
            
            if response.status_code == 200:
                registros = response.json()
                total_registros = len(registros)
                print(f"Hay un total de {total_registros} registros.")
    
                if total_registros > 0:
                    registro_id = int(input("Por favor, introduce el ID del registro que quieres visualizar: "))
    
                    if registro_id > 0 and registro_id <= total_registros:
                        registro = registros[registro_id - 1]
                        print(f"\nID: {registro['id']}")
                        for field in endpoints[opcion]["fields"]:
                            if field in registro:
                                if field == "address":
                                    address = registro[field]
                                    print(f"Dirección: {address['street']}, {address['suite']}, {address['city']}, {address['zipcode']}")
                                elif field == "company":
                                    company = registro[field]
                                    print(f"Empresa: {company['name']}")
                                    print(f"Frase clave: {company['catchPhrase']}")
                                    print(f"Servicios: {company['bs']}")
                                else:
                                    print(f"{field.capitalize()}: {registro[field]}")
                                    
                        print("------")
                        input('Presiona Enter para volver al menu...')
                    else:
                        print("Has introducido un número de registro inválido.")
                        input('Presiona Enter para volver al menu...')
                else:
                    print("No hay registros para mostrar.")
                    input('Presiona Enter para volver al menu...')
            else:
                print(f"Error al obtener los datos desde el endpoint: {endpoint}")
                input('Presiona Enter para volver al menu...')
        else:
            print("Opción inválida. Por favor, elige una opción válida.")
            input('Presiona Enter para volver al menu...')
    limpiar_pantalla()
    print("¡Hasta luego!")

if __name__ == "__main__":
    main()
    
