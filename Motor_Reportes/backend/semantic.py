class AnalizadorSemanticoVulnerabilidades:
    def evaluar_semantica(self, datos_estructurados):
        """Evalúa el árbol dinámico multilínea para determinar el nivel corporativo de riesgo (OE3 y OE4)"""

        # Fallback inmediato si el filtro sintáctico detecta ruido o texto irrelevante ("Hola")
        if not datos_estructurados["tiene_datos_validos"]:
            return {
                "valido": False,
                "nivel_riesgo": "NO IDENTIFICADO",
                "nivel_prioridad": "NULA - Texto irrelevante",
                "regla_aplicada": "Filtro de Excepciones: El texto analizado no contiene ningún patrón de ciberseguridad."
            }

        # 1. Extracción directa de las severidades registradas en la tabla de la Fase 2
        lista_severidades = [comp["valor"] for comp in datos_estructurados["componentes_encontrados"] if
                             comp["categoria"] == "Nivel de Criticidad"]

        # 2. Identificación de impacto máximo independiente de la gramática
        es_critico = "CRITICAL" in lista_severidades or datos_estructurados.get("estado_critico", False)
        es_alto = "HIGH" in lista_severidades

        # 3. Volumen de relaciones gramaticales (Fase 2)
        cantidad_relaciones = len(datos_estructurados["relaciones_contextuales"])

        # ======================================================================
        # MOTOR DE REGLAS SEMÁNTICAS DE PRIORIZACIÓN (Cumplimiento OE3 y OE4)
        # ======================================================================
        if es_critico:
            nivel_riesgo = "CRÍTICO (Vulnerabilidad máxima confirmada)"
            nivel_prioridad = "ALTA - Intervención inmediata del equipo DevSecOps"
            regla_activada = "Regla 1: Criticidad explícita máxima detectada en los tokens del reporte."

        elif es_alto:
            nivel_riesgo = "ALTO (Riesgo inminente de intrusión o caída)"
            nivel_prioridad = "MEDIA/ALTA - Aplicación de parches dentro de las próximas 24 horas"
            regla_activada = "Regla 2: Nivel de severidad Alto explícitamente declarado en el sistema."

        elif cantidad_relaciones >= 2:
            nivel_riesgo = "MEDIO/ALTO (Vectores de ataque múltiples encadenados)"
            nivel_prioridad = "MEDIA - Análisis profundo requerido"
            regla_activada = "Regla 3: Múltiples dependencias gramaticales de riesgo detectadas simultáneamente."

        elif cantidad_relaciones == 1:
            nivel_riesgo = "MEDIO (Comportamiento anómalo aislado)"
            nivel_prioridad = "MEDIA - Monitoreo preventivo y revisión de logs"
            regla_activada = "Regla 4: Estructura sintáctica válida con un indicador de peligro latente."

        else:
            nivel_riesgo = "BAJO (Incidente aislado / Informativo)"
            nivel_prioridad = "BAJA - Registro preventivo en la bitácora de eventos"
            regla_activada = "Regla 5: Datos técnicos recolectados sin dependencias gramaticales de gravedad."

        return {
            "valido": True,
            "nivel_riesgo": nivel_riesgo,
            "nivel_prioridad": nivel_prioridad,
            "regla_aplicada": regla_activada
        }