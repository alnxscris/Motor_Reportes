class AnalizadorSintacticoVulnerabilidades:
    def analizar_sintaxis(self, lista_tokens):
        """Transforma la secuencia de tokens en un árbol sintáctico puramente dinámico y multilínea"""

        # Estructura limpia y adaptable sin categorías preestablecidas fijas
        reporte_estructurado = {
            "componentes_encontrados": [],
            "relaciones_contextuales": [],
            "estado_critico": False,
            "tiene_datos_validos": False
        }

        # Conjuntos temporales para control de duplicados lógicos en la visualización
        elementos_registrados = set()
        longitud = len(lista_tokens)

        # ======================================================================
        # PIVOTE 1: DETECCIÓN Y CLASIFICACIÓN ADAPTATIVA DE COMPONENTES
        # ======================================================================
        for token in lista_tokens:
            tipo = token['tipo']
            valor = token['valor']

            # Ignoramos elementos vacíos o residuales
            if tipo in ['IGNORAR', 'OTROS']:
                continue

            # Si detectamos cualquier token de seguridad válido, activamos la métrica de confianza
            reporte_estructurado["tiene_datos_validos"] = True

            if tipo == 'SEVERIDAD' and valor == 'CRITICAL':
                reporte_estructurado["estado_critico"] = True

            # Creamos una llave única para evitar registrar exactamente el mismo componente en la tabla
            llave_duplicado = f"{tipo}:{valor}"
            if llave_duplicado not in elementos_registrados:
                elementos_registrados.add(llave_duplicado)

                # Mapeo de nombres legibles para el usuario final según el tipo de token
                nombre_legible = tipo
                if tipo in ['CVE', 'CWE', 'CNVD', 'JVNDB']:
                    nombre_legible = f"Firma Global ({tipo})"
                elif tipo == 'IP':
                    nombre_legible = "Dirección IP"
                elif tipo == 'PUERTO':
                    nombre_legible = "Puerto de Conexión"
                elif tipo == 'ACTIVO':
                    nombre_legible = "Componente de Infraestructura"
                elif tipo == 'ESTADO':
                    nombre_legible = "Estado o Vulnerabilidad de Sistema"
                elif tipo == 'SEVERIDAD':
                    nombre_legible = "Nivel de Criticidad"

                # Limpieza visual del valor del puerto (extrae p.ej. '80' de 'puerto 80')
                valor_limpio = "".join(filter(str.isdigit, valor)) if tipo == 'PUERTO' else valor

                # Insertamos una nueva fila de componente de manera 100% dinámica
                reporte_estructurado["componentes_encontrados"].append({
                    "categoria": nombre_legible,
                    "valor": valor_limpio
                })

        # ======================================================================
        # PIVOTE 2: ANÁLISIS GRAMATICAL MULTI-ÁRBOL (Detección de patrones en cadena)
        # ======================================================================
        for i in range(longitud):
            token_actual = lista_tokens[i]

            # Patrón A: [ACTIVO] + [ESTADO] -> (Ej: "base de datos sufrió una caida")
            if token_actual['tipo'] == 'ACTIVO' and (i + 1 < longitud):
                siguiente = lista_tokens[i + 1]
                if siguiente['tipo'] == 'ESTADO':
                    reporte_estructurado["relaciones_contextuales"].append({
                        "tipo_relacion": "Infraestructura Afectada",
                        "descripcion": f"El componente <strong>{token_actual['valor'].lower()}</strong> fue asociado directamente con la vulnerabilidad o comportamiento: <em>{siguiente['valor'].lower()}</em>."
                    })

            # Patrón B: [IP] + [PUERTO] -> (Ej: "192.168.1.1 puerto 443")
            if token_actual['tipo'] == 'IP' and (i + 1 < longitud):
                siguiente = lista_tokens[i + 1]
                if siguiente['tipo'] == 'PUERTO':
                    puerto_digitos = "".join(filter(str.isdigit, siguiente['valor']))
                    reporte_estructurado["relaciones_contextuales"].append({
                        "tipo_relacion": "Asociación de Red",
                        "descripcion": f"Se identificó un vector de conexión vinculando la dirección IP <strong>{token_actual['valor']}</strong> a través del puerto activo <strong>{puerto_digitos}</strong>."
                    })

            # Patrón C: [CVE/CWE/CNVD] + [SEVERIDAD] -> (Ej: "CWE-120 severidad CRITICAL")
            if token_actual['tipo'] in ['CVE', 'CWE', 'CNVD', 'JVNDB'] and (i + 1 < longitud):
                siguiente = lista_tokens[i + 1]
                if siguiente['tipo'] == 'SEVERIDAD':
                    reporte_estructurado["relaciones_contextuales"].append({
                        "tipo_relacion": "Validación de Firma",
                        "descripcion": f"La debilidad catalogada como <strong>{token_actual['valor']}</strong> ha sido ratificada formalmente bajo el impacto <strong>{siguiente['valor']}</strong>."
                    })

        return reporte_estructurado