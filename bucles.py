
""" Leer un número y determinar si es primo (solo divisible entre 1 y él mismo).
1
Entender el problema
Antes de escribir una sola línea, separa el problema en sus tres partes.

Entrada — qué me dan
n (entero)
Proceso — qué hago con eso
probar divisores de 2 hasta √n usando bandera
Salida — qué debo mostrar
"n es primo" o "n no es primo"
Ejemplo de entrada
n = 17
Salida esperada
17 es primo
2
Bosquejo a mano
Resuélvelo como lo harías en el cuaderno, sin pensar en código. Aquí es donde aparece el patrón.

✍️ En el cuaderno
n = 17, es_primo = True (bandera)

Pruebo divisores del 2 al √17 ≈ 4:
  n    c=2
 mientras c < n and es_primo:
  si n % c == 0: (no divide)
    es_primo = False
  c = c +1
 finMientras
 N    C=2
 Mientras c < n:
  si N % C = 0
    es_primo = False
  sino  
    C = C +1
 finMientras
 si es_primo:
  print(n," es primo")
 sino
    print(n," NO es primo")

  17 % 3 = 2 (no divide)
  17 % 4 = 1 (no divide)
  ......
  17 % 16 = 0 (no divide)
     17 salgo y es primo)=True
n=9
  9 % 2 = 1 (no divide)
  9 % 3 = 0 (divide) → es_primo = False,


Ninguno dividió → 17 es primo ✓
3
Descubrir el patrón
💡 Aquí nos damos cuenta de que…
Aquí usamos el patrón bandera: una variable booleana que empieza en True y cambia a False apenas se descarta.

Optimización clave: solo hace falta probar hasta √n, no hasta n. Si n tiene un divisor mayor que √n, forzosamente tiene otro menor que ya habríamos encontrado.

Un caso especial: 0 y 1 no son primos. Se descarta al inicio.
 """

def primoFor(n):
    es_primo = True                     # BANDERA: asumimos que sí
    if n < 2:
        es_primo = False                # 0 y 1 no son primos
    else:
        # Probar divisores del 2 hasta √n
        for i in range(2, n):
            if n % i == 0:              # si i divide exacto a n...
                es_primo = False        # ...no es primo
                break                   # optimización: no seguir probando

    if es_primo:
        print(f"{n} es primo")
    else:
        print(f"{n} NO es primo")

def primoWhile(n):
    es_primo = True                     # BANDERA: asumimos que sí

    if n < 2:
        es_primo = False                # 0 y 1 no son primos
    else:
        # Probar divisores del 2 hasta √n
        i=2
        lim = int(n/2)+1
        while i < lim and es_primo:
            if n % i == 0: es_primo = False  
            else:i = i + 1                   # optimización: no seguir probando

    if es_primo:
        print(f"{n} es primo")
    else:
        print(f"{n} NO es primo")
# return true si es primo, false si no lo es
def primo(n):
    es_primo = True                     # BANDERA: asumimos que sí

    if n < 2:
        es_primo = False                # 0 y 1 no son primos
    else:
        # Probar divisores del 2 hasta √n
        i=2
        lim = int(n/2)+1
        while i < lim and es_primo:
            if n % i == 0: es_primo = False  
            else:i = i + 1                   # optimización: no seguir probando

    return es_primo

n = int(input("Número: "))
primoFor(n)
for n in range(2,101):
    if primoWhile(n):
        print(f"{n} es primo")
    else:
        print(f"{n} NO es primo")

primos=[]
for n in range(2,101):
    if not primoWhile(n):
        primos.append(n)
   
