from functools import wraps

def repetir(veces):
    """Decorador que repite la función N veces."""
    def decorador(func):
        @wraps(func)
        def envoltorio(*args, **kwargs):
            for _ in range(veces):
                resultado = func(*args, **kwargs)
            return resultado
        return envoltorio
    return decorador


@repetir(3)
def saludar(nombre):
    print(f"Hola {nombre}")


saludar("Ana")
# Hola Ana
# Hola Ana
# Hola Ana

# Es equivalente a:
# saludar = repetir(3)(saludar)