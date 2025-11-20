from collections import Counter
import random
import math

N_NUMEROS = 30    
DECIMALES = 5       
CONFIANZA = 0.95   

# Valor crítico de chi-cuadrado para:
CHI2_CRITICO_95_G6 = 12.5916

# (sobre 10^5 combinaciones posibles)
PROBS = {
    "todos_distintos": 0.3024,
    "un_par":          0.5040,
    "dos_pares":       0.1080,
    "tercia":          0.0720,
    "full_house":      0.0090,
    "poker":           0.0045,
    "quintilla":       0.0001,
}

# Para impresión bonita en español y en el orden de la tabla
DISPLAY_ORDER = [
    "dos_pares",
    "full_house",
    "poker",
    "quintilla",
    "tercia",
    "todos_distintos",
    "un_par",
]

DISPLAY_NAME = {
    "todos_distintos": "TODOS DIFERENTES",
    "un_par":          "UN PAR",
    "dos_pares":       "DOS PARES",
    "tercia":          "TERCIA",
    "full_house":      "FULL HOUSE",
    "poker":           "POKER",
    "quintilla":       "QUINTILLA",
}


def extraer_digitos(u: float, k: int = 5) -> str:
    """Devuelve los primeros k dígitos decimales de un número en [0,1)."""
    n = int(u * (10 ** k))
    return f"{n:0{k}d}"


def clasificar_poker(digitos: str) -> str:
    """Clasifica una cadena de 5 dígitos en categoría de póker."""
    c = Counter(digitos)
    rep = sorted(c.values(), reverse=True)

    if rep == [1, 1, 1, 1, 1]:
        return "todos_distintos"
    if rep == [2, 1, 1, 1]:
        return "un_par"
    if rep == [2, 2, 1]:
        return "dos_pares"
    if rep == [3, 1, 1]:
        return "tercia"
    if rep == [3, 2]:
        return "full_house"
    if rep == [4, 1]:
        return "poker"
    if rep == [5]:
        return "quintilla"
    return "otra"


def prueba_poker(numeros, k=5):
    """Realiza la prueba de póker y retorna todo lo necesario para imprimir tablas."""
    n = len(numeros)

    # 1) Clasificar cada número
    clasificaciones = []
    for u in numeros:
        d = extraer_digitos(u, k)
        cat = clasificar_poker(d)
        clasificaciones.append((u, cat))

    # 2) Frecuencias observadas
    conteo = Counter(cat for _, cat in clasificaciones)
    # asegurar todas las categorías
    for cat in PROBS.keys():
        conteo.setdefault(cat, 0)

    # 3) Frecuencias esperadas
    esperadas = {cat: n * p for cat, p in PROBS.items()}

    # 4) Chi-cuadrado
    chi2 = 0.0
    contribuciones = {}
    for cat in PROBS.keys():
        o = conteo[cat]
        e = esperadas[cat]
        c = (e - o) ** 2 / e if e > 0 else 0
        chi2 += c
        contribuciones[cat] = c

    gl = len(PROBS) - 1
    return {
        "clasificaciones": clasificaciones,
        "observadas": conteo,
        "esperadas": esperadas,
        "contribuciones": contribuciones,
        "chi2": chi2,
        "gl": gl,
    }

def imprimir_encabezado():
    print("=" * 68)
    print("PRUEBA DE PÓKER - GENERADOR DE NÚMEROS ALEATORIOS".center(68))
    print("=" * 68)
    print(f"Nivel de confianza: {CONFIANZA*100:.1f}%")
    print(f"Total de números : {N_NUMEROS}")
    print(f"Decimales        : {DECIMALES}")
    print("=" * 68)


def imprimir_tabla_numeros(numeros, por_fila=6):
    print("TABLA 1: NÚMEROS ALEATORIOS")
    print("-" * 68)
    fila = 1
    for i in range(0, len(numeros), por_fila):
        chunk = numeros[i:i+por_fila]
        print(f"Fila {fila:2d}: ", end="")
        for u in chunk:
            print(f"{u:.{DECIMALES}f}  ", end="")
        print()
        fila += 1
    print("=" * 68)


def imprimir_tabla_categorizados(datos, por_fila=6):
    """
    datos: lista de (numero, categoria)
    """
    print("TABLA 2: NÚMEROS CATEGORIZADOS")
    print("-" * 68)
    fila = 1
    for i in range(0, len(datos), por_fila):
        chunk = datos[i:i+por_fila]

        # línea de números
        print(f"Fila {fila:2d}: Números:   ", end="")
        for u, _ in chunk:
            print(f"{u:.{DECIMALES}f}  ", end="")
        print()

        # línea de categorías
        print(f"       Categoría:", end=" ")
        for _, cat in chunk:
            nombre = DISPLAY_NAME.get(cat, cat).ljust(14)
            print(nombre, end=" ")
        print("\n")
        fila += 1
    print("=" * 68)


def imprimir_tabla_criticos(gl):
    alpha = 1 - CONFIANZA
    chi2_crit = CHI2_CRITICO_95_G6  # en este ejemplo gl=6 fijo
    print("TABLA 3: VALORES CRÍTICOS DE CHI-CUADRADO")
    print("-" * 68)
    print(f"Nivel de confianza: {CONFIANZA*100:.1f}%")
    print(f"Alpha (α)         : {alpha}")
    print(f"Grados de libertad: {gl}")
    print(f"χ²(α, gl)         : {chi2_crit:.4f}")
    print("=" * 68)
    return chi2_crit


def imprimir_tabla_frecuencias(obs, esp, contrib):
    print("TABLA 4: FRECUENCIAS OBSERVADAS Y ESPERADAS")
    print("-" * 68)
    print(f"{'Categoría':15s} {'O_i':>6s} {'E_i':>8s} {'P_i':>8s} {'(E_i - O_i)^2/E_i':>18s}")
    for cat in DISPLAY_ORDER:
        nombre = DISPLAY_NAME[cat]
        o = obs[cat]
        e = esp[cat]
        p = PROBS[cat]
        c = contrib[cat]
        print(f"{nombre:15s} {o:6d} {e:8.2f} {p:8.4f} {c:18.4f}")
    print("=" * 68)


def imprimir_resultado(chi2, chi2_crit, gl):
    print("TABLA 5: RESULTADO Y DECISIÓN")
    print("-" * 68)
    print(f"Estadístico calculado (χ²_o): {chi2:.4f}")
    print(f"Estadístico crítico  (χ²_c): {chi2_crit:.4f}")
    print(f"Grados de libertad           : {gl}")
    print()

    if chi2 <= chi2_crit:
        print("✅ DECISIÓN: NO se rechaza la hipótesis nula.")
        print("   Los números pasan la prueba de póker (se aceptan como independientes).")
    else:
        print("❌ DECISIÓN: SE RECHAZA la hipótesis nula.")
        print("   Los números NO pasan la prueba de póker (no se consideran independientes).")
    print("=" * 68)


if __name__ == "__main__":
    numeros = [random.random() for _ in range(N_NUMEROS)]
    resultado = prueba_poker(numeros, k=DECIMALES)
    imprimir_encabezado()
    imprimir_tabla_numeros(numeros)
    imprimir_tabla_categorizados(resultado["clasificaciones"])
    chi2_crit = imprimir_tabla_criticos(resultado["gl"])
    imprimir_tabla_frecuencias(
        resultado["observadas"],
        resultado["esperadas"],
        resultado["contribuciones"],
    )
    imprimir_resultado(resultado["chi2"], chi2_crit, resultado["gl"])


    # numeros = [
    #     0.11111, 0.11112, 0.11113, 0.11114, 0.11115,
    #     0.22221, 0.22222, 0.22223, 0.22224, 0.22225,
    #     0.33331, 0.33332, 0.33333, 0.33334, 0.33335,
    #     0.44441, 0.44442, 0.44443, 0.44444, 0.44445,
    #     0.55551, 0.55552, 0.55553, 0.55554, 0.55555,
    #     0.66661, 0.66662, 0.66663, 0.66664, 0.66665,
    # ]