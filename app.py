"""
Prueba de Póker para números pseudoaleatorios
Autor: (tu nombre)
Descripción:
    - Clasifica cada número según sus decimales (como mano de póker).
    - Calcula frecuencias observadas y esperadas.
    - Calcula el estadístico Chi-cuadrado.
    - Compara con el valor crítico y decide si los datos pasan la prueba.
"""

from collections import Counter

# Probabilidades teóricas de las diapositivas
POKER_PROBS = {
    5: {  # 5 decimales -> 7 categorías
        "TD": 0.3024,  # Todos diferentes
        "1P": 0.5040,  # Exactamente 1 par
        "2P": 0.1080,  # Dos pares
        "TP": 0.0090,  # Tercia y par
        "T":  0.0720,  # Tercia
        "P":  0.0045,  # Póker
        "Q":  0.0001,  # Quintilla
    },
    4: {  # 4 decimales -> 5 categorías
        "TD": 0.5040,
        "1P": 0.4320,
        "2P": 0.0270,
        "T":  0.0360,
        "P":  0.0010,
    },
    3: {  # 3 decimales -> 3 categorías
        "TD": 0.72,
        "1P": 0.27,
        "T":  0.01,
    }
}

# Valores críticos de Chi-cuadrado para alfa = 0.05 y m-1 g.l.
# (m = número de categorías, según diapositivas)
CHI_CRIT = {
    3: 5.991,   # m=3  -> gl=2
    4: 9.488,   # m=5  -> gl=4
    5: 12.592,  # m=7  -> gl=6  (diapositiva: 12,5916)
}


def clasificar_mano(digitos: str) -> str:
    """
    Recibe un string con los dígitos decimales (ej. '06141')
    y devuelve la categoría de póker:
        TD, 1P, 2P, T, TP, P, Q
    según los patrones de repetición.
    """
    conteos = Counter(digitos)
    patron = sorted(conteos.values(), reverse=True)  # ej. [2,1,1,1]

    if len(digitos) == 5:
        if patron == [1, 1, 1, 1, 1]:
            return "TD"
        if patron == [2, 1, 1, 1]:
            return "1P"
        if patron == [2, 2, 1]:
            return "2P"
        if patron == [3, 1, 1]:
            return "T"
        if patron == [3, 2]:
            return "TP"
        if patron == [4, 1]:
            return "P"
        if patron == [5]:
            return "Q"

    elif len(digitos) == 4:
        if patron == [1, 1, 1, 1]:
            return "TD"
        if patron == [2, 1, 1]:
            return "1P"
        if patron == [2, 2]:
            return "2P"
        if patron == [3, 1]:
            return "T"
        if patron == [4]:
            return "P"

    elif len(digitos) == 3:
        if patron == [1, 1, 1]:
            return "TD"
        if patron == [2, 1]:
            return "1P"
        if patron == [3]:
            return "T"

    # Si algo raro pasa:
    raise ValueError(f"No se pudo clasificar la mano: {digitos} (patrón {patron})")


def prueba_poker(numeros, decimales=5, alpha=0.05):
    """
    Ejecuta la prueba de póker.

    :param numeros: lista de números en (0,1)
    :param decimales: número de decimales a considerar (3, 4 o 5)
    :param alpha: nivel de significancia (solo informativo)
    :return: diccionario con resultados
    """
    if decimales not in POKER_PROBS:
        raise ValueError("decimales debe ser 3, 4 o 5.")

    probs = POKER_PROBS[decimales]
    categorias = {cat: 0 for cat in probs.keys()}

    # 1) Clasificar cada número y contar frecuencias observadas
    for x in numeros:
        s = f"{float(x):.{decimales}f}"   # lo formateo con d decimales fijos
        digitos = s.split(".")[1][:decimales]
        cat = clasificar_mano(digitos)
        categorias[cat] += 1

    n = len(numeros)

    # 2) Calcular Ei y el chi-cuadrado
    chi2 = 0.0
    tabla = []
    for cat, p in probs.items():
        Oi = categorias[cat]
        Ei = n * p
        chi2 += (Oi - Ei) ** 2 / Ei
        tabla.append((cat, p, Oi, Ei))

    m = len(probs)      # número de categorías
    gl = m - 1          # grados de libertad
    chi_critico = CHI_CRIT[decimales]
    pasa = chi2 < chi_critico

    return {
        "n": n,
        "decimales": decimales,
        "alpha": alpha,
        "tabla": tabla,
        "chi2": chi2,
        "gl": gl,
        "chi_critico": chi_critico,
        "pasa": pasa
    }


def imprimir_resultados(res):
    """
    Muestra los resultados en forma de tabla y el veredicto final.
    """
    print("===== PRUEBA DE PÓKER =====")
    print(f"Números analizados (n): {res['n']}")
    print(f"Decimales considerados: {res['decimales']}")
    print(f"Nivel de significancia α: {res['alpha']}")
    print()

    # Tabla de resultados
    print("Categoría | Probabilidad p_i | Frec. observada O_i | Frec. esperada E_i")
    print("--------------------------------------------------------------------------")
    for cat, p, Oi, Ei in res["tabla"]:
        print(f"{cat:8} | {p:16.4f} | {Oi:19d} | {Ei:16.4f}")
    print("--------------------------------------------------------------------------")
    print(f"χ² calculado = {res['chi2']:.4f}")
    print(f"χ² crítico   = {res['chi_critico']:.4f}  (gl = {res['gl']})")
    print()

    if res["pasa"]:
        print("Conclusión: χ² calculado < χ² crítico → NO se rechaza la hipótesis.")
        print("Los números CUMPLEN la prueba de póker para el nivel de significancia dado.")
    else:
        print("Conclusión: χ² calculado ≥ χ² crítico → Se rechaza la hipótesis.")
        print("Los números NO cumplen la prueba de póker para el nivel de significancia dado.")


# ---------------------------------------------------------------------
# EJECUCIÓN PRINCIPAL
# ---------------------------------------------------------------------
if __name__ == "__main__":
    # TODO: aquí debes poner los datos numéricos de la clase.
    # EJEMPLO (cámbialos por los que te dio el profesor):
    numeros_clase = [
        0.06141, 0.72484, 0.94107, 0.56766, 0.14411, 0.87648,
        0.81792, 0.48999, 0.18590, 0.06060, 0.11223, 0.64794,
        0.52953, 0.50502, 0.30444, 0.70688, 0.25357, 0.31555,
        0.04127, 0.67347, 0.28103, 0.99367, 0.44598, 0.73997,
        0.27813, 0.62182, 0.82578, 0.85923, 0.51483, 0.09099,
    ]

    # Cambia decimales=5 si tu prueba está definida para 3 o 4 decimales
    resultados = prueba_poker(numeros_clase, decimales=5, alpha=0.05)
    imprimir_resultados(resultados)
