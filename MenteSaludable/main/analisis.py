def analizar_resultados(puntuaciones):
    """Analiza los resultados de la evaluación con escala de 1 (mal) a 5 (bien)"""
    recomendaciones = []

    # EM - Emociones
    em = puntuaciones.get('EM', 0)
    if em < 2:
        recomendaciones.append("🔴 Tus emociones han estado muy desequilibradas esta semana.")
    elif em < 3.5:
        recomendaciones.append("🟡 Algunas dificultades emocionales detectadas. Prueba escribir un diario emocional.")
    else:
        recomendaciones.append("🟢 Emocionalmente te has sentido estable. ¡Sigue así!")

    # EN - Energía y Motivación
    en = puntuaciones.get('EN', 0)
    if en < 2:
        recomendaciones.append("🔴 Niveles de energía muy bajos. Revisa tu descanso y alimentación.")
    elif en < 3.5:
        recomendaciones.append("🟡 Podrías mejorar tu motivación. Establece metas pequeñas cada día.")
    else:
        recomendaciones.append("🟢 Buena energía y motivación. ¡Bien hecho!")

    # RE - Relaciones
    re = puntuaciones.get('RE', 0)
    if re < 2:
        recomendaciones.append("🔴 Problemas significativos en tus relaciones. Considera hablar con alguien de confianza.")
    elif re < 3.5:
        recomendaciones.append("🟡 Algunas tensiones sociales detectadas. Intenta fortalecer tus vínculos.")
    else:
        recomendaciones.append("🟢 Relaciones saludables. ¡Disfrútalas!")

    # HB - Hábitos y Cuidado Personal
    hb = puntuaciones.get('HB', 0)
    if hb < 2:
        recomendaciones.append("🔴 Hábitos poco saludables. Enfócate en tu autocuidado.")
    elif hb < 3.5:
        recomendaciones.append("🟡 Algunos hábitos podrían mejorar. Comienza con rutinas sencillas.")
    else:
        recomendaciones.append("🟢 Buenos hábitos de cuidado personal. ¡Excelente trabajo!")

    # PE - Pensamientos y Perspectiva
    pe = puntuaciones.get('PE', 0)
    if pe < 2:
        recomendaciones.append("🔴 Pensamientos negativos dominantes. Prueba técnicas de reestructuración cognitiva.")
    elif pe < 3.5:
        recomendaciones.append("🟡 Algunas dificultades con tu perspectiva. Practica gratitud diaria.")
    else:
        recomendaciones.append("🟢 Perspectiva mental positiva. ¡Muy bien!")

    # ES - Estrés y Manejo
    es = puntuaciones.get('ES', 0)
    if es < 2:
        recomendaciones.append("🔴 Altos niveles de estrés. Es urgente incorporar estrategias de relajación.")
    elif es < 3.5:
        recomendaciones.append("🟡 Estrés moderado. Intenta ejercicios de respiración consciente.")
    else:
        recomendaciones.append("🟢 Buen manejo del estrés. Continúa así.")

    return "\n".join(recomendaciones)
