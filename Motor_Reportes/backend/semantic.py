class AnalizadorSemanticoVulnerabilidades:
    def evaluar_semantica(self, datos_estructurados):
        """Evalúa el árbol dinámico multilínea para determinar el nivel corporativo de riesgo"""

        # Fallback inmediato si el filtro sintáctico detecta ruido o texto irrelevante ("Hola")
        if not datos_estructurados["tiene_datos_validos"]:
            return {
                "valido": False,
                "nivel_riesgo": "NO IDENTIFICADO",
                "nivel_prioridad": "NULA - Texto irrelevante",
                "regla_aplicada": "Filtro de Excepciones: El texto analizado no contiene ningún patrón de ciberseguridad."
            }

        # Evaluación semántica basada en el volumen de relaciones gramaticales encontradas
        cantidad_relaciones = len(datos_estructurados["relaciones_contextuales"])
        es_critico = datos_estructurados["estado_critico"]

        if es_critico and cantidad_relaciones >= 2:
            nivel_riesgo = "CRÍTICO (Múltiples vectores de ataque confirmados en vivo)"
            nivel_prioridad = "ALTA - Intervención inmediata del equipo DevSecOps"
            regla_activada = "Regla 1: Coincidencia multi-fase de severidad máxima con activos vinculados."
        elif es_critico or cantidad_relaciones >= 1:
            nivel_riesgo = "ALTO (Riesgo contextualizado de intrusión)"
            nivel_prioridad = "MEDIA - Aplicación de parches dentro de las próximas 24 horas"
            regla_activada = "Regla 2: Estructura sintáctica válida con indicadores de peligro latente."
        else:
            nivel_riesgo = "BAJO (Incidente aislado / Informativo)"
            nivel_prioridad = "BAJA - Registro preventivo en la bitácora de eventos"
            regla_activada = "Regla 3: Datos técnicos recolectados sin dependencias gramaticales de riesgo."

        return {
            "valido": True,
            "nivel_riesgo": nivel_riesgo,
            "nivel_prioridad": nivel_prioridad,
            "regla_aplicada": regla_activada
        }