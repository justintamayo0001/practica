# 1. En Python las funciones son objetos: se pueden pasar como argumento
def mi_funcion(nombre):
    print(f"Hola, {nombre}")
 # Llamada directa
def ejecutar(f):
    nom = input("Ingrese su nombre: ")
    f(nom)

#ejecutar(mi_funcion) 

# 2. Un decorador es una función que RECIBE una función y RETORNA otra
def con_log(func):
    def envoltorio():
        print(f">>> antes de llamar a {func.__name__}")
        func()
        print(f"<<< después de llamar a {func.__name__}")
    return envoltorio


# 3. Uso "a la antigua":
def saludar():
    print("Hola mundo")

#saludar = con_log(saludar)    # reemplazo saludar por la versión envuelta
#saludar()
# >>> antes de llamar a saludar
# Hola mundo
# <<< después de llamar a saludar


# 4. La sintaxis @ es azúcar sintáctico para lo mismo
@con_log
def despedir():
    print("Adiós")

despedir() 

###########
import time
from functools import wraps

def cronometrar(func):
    @wraps(func)                          # preserva nombre y docstring de func
    def envoltorio(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fin = time.time()
        print(f"[{func.__name__}] tardó {fin - inicio:.4f}s")
        return resultado
    return envoltorio


@cronometrar
def sumar_grandes(n):
    """Suma del 1 al n."""
    total = 0
    for i in range(n):
        total += i
    return total


r = sumar_grandes(10)
# [sumar_grandes] tardó 0.0523s
print(sumar_grandes.__name__)             # 'sumar_grandes' (gracias a @wraps)     # Automáticamente aplicado con_log