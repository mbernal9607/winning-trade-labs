from casaHeberth import Cocina


# Definición de un decorador
def mi_decorador(func):
    def wrapper():
        print("Antes de llamar a la función")
        func()
        print("Después de llamar a la función")


    return wrapper

# Uso del decorador
@mi_decorador
def mi_funcion():
    print("¡Hola, mundo!")

# Llamada a la función decorada
mi_funcion()