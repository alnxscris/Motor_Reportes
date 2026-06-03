import re


class AnalizadorLexicoVulnerabilidades:
    def __init__(self):
        # DICCIONARIO LÉXICO INDESTRUCTIBLE: INGLÉS, ESPAÑOL Y CONCEPTOS CWE (OE1) [cite: 33, 383]
        self.reglas_tokens = [
            # 1. IDENTIFICADORES DE BASES DE DATOS Y DEBILIDADES [cite: 47, 383]
            ('CVE', r'\bCVE-\d{4}-\d{4,7}\b'),  # Estándar global de vulnerabilidades [cite: 47]
            ('CNVD', r'\bCNVD-\d{5}\b'),  # Registro de Asia/China [cite: 47]
            ('JVNDB', r'\bJVNDB-\d{4}-\d{6}\b'),  # Registro de Japón [cite: 47]
            ('CWE', r'\bCWE-\d{1,5}\b'),  # Estándar de debilidades de software

            # 2. NIVELES DE SEVERIDAD Y CRITICIDAD (Bilingüe completo)
            ('SEVERIDAD', r'\b('
                          r'CRITICAL|CRÍTICO|CRÍTICA|CRITICO|URGENTE|EMERGENCIA|SEVERO|SEVERA|'
                          r'HIGH|ALTO|ALTA|MODERATE|MODERADO|MODERADA|'
                          r'MEDIUM|MEDIO|MEDIA|MEDIUM|LOW|BAJO|BAJA|MINIMAL|MÍNIMO|MÍNIMA|'
                          r'INFORMATIVO|INFORMATIVA|INFO|ADVISORY'
                          r')\b'),

            # 3. DIRECCIONES IP (Identificación de infraestructura)
            ('IP', r'\b\d{1,3}(?:\.\d{1,3}){3}\b'),

            # 4. PUERTOS DE RED Y ENLACES
            ('PUERTO', r'\b(puertos?|ports?|p\:|pt?)\s*\d{1,5}\b'),

            # 5. ACTIVOS TECNOLÓGICOS Y INFRAESTRUCTURA (Hardware, Cloud y Sistemas)
            ('ACTIVO', r'\b('
                       r'servidor(es)?|server(s)?|database(s)?|bd|base(s)?\s+de\s+datos|cluster(s)?|instancia(s)?|'
                       r'firewall(s)?|cortafuegos|ids|ips|waf|proxy|routers?|enrutador(es)?|switch(es)?|conmutador(es)?|'
                       r'api(s)?|endpoint(s)?|microservicio(s)?|backend|frontend|web(site)?|pagina(s)?|'
                       r'app(s)?|aplicacion(es)?|software|firmware|middleware|kernel|sistema(s)?|operativo(s)?|'
                       r'host(s)?|anfitrion(es)?|pc|computadora(s)?|laptop(s)?|dispositivo(s)?|device(s)?|'
                       r'cloud|nube|aws|azure|gcp|docker|kubernetes|k8s|contenedor(es)?|vms?|maquina(s)?\s+virtual(es)?|'
                       r'red|subred|vlan|active\s+directory|ad|directorio\s+activo|controlador\s+de\s+dominio|'
                       r'linux|ubuntu|debian|centos|redhat|rhel|windows(server)?|iis|apache|nginx|tomcat|'
                       r'microcodigo|bios|routeros|cisco|fortinet|pfsense|sso|iam|oauth|saml'
                       r')\b'),

            # 6. PROBLEMAS DE SOFTWARE Y SISTEMA (INGLÉS + ESPAÑOL MASTRICULADO)
            ('ESTADO', r'\b('
            # Fallos de Memoria y Desbordamientos
                       r'vulnerable(s)?|fallos?|defectos?|brecha(s)?|hole(s)?|fuga(s)?|filtrado(s)?|exfiltracion|'
                       r'abierto(s)?|open|listening|escucha|comprometido(s)?|afectado(s)?|infectado(s)?|'
                       r'explotado(s)?|hackeado(s)?|atacado(s)?|vulnerado(s)?|detectado(s)?|identificado(s)?|'
                       r'activo(s)?|active|running|ejecucion|alerta(s)?|warning|danger|peligro|riesgo(s)?|'
                       r'overflow|desbordamiento(s)?|buffer|stack|heap|memory\s+leak|fuga(s)?\s+de\s+memoria|'
                       r'corrupcion\s+de\s+memoria|memory\s+corruption|out\s+of\s+bounds|fuera\s+de\s+limites|'
                       r'use\s+after\s+free|uso\s+despues\s+de\s+liberar|null\s+pointer|puntero(s)?\s+nulo(s)?|'
                       r'dereference|desreferenciacion|integer\s+overflow|desbordamiento\s+de\s+entero|'
                       r'race\s+condition|condicion(es)?\s+de\s+carrera|'
            # Inyecciones y Manipulación de Datos
                       r'malware|virus|troyano(s)?|trojan|ransomware|secuestro|backdoor(s)?|puerta(s)?\s+trasera(s)?|'
                       r'spyware|rootkit|exploit(s)?|payload(s)?|zero-day|0-day|dia\s+cero|'
                       r'dos|ddos|denegacion\s+de\s+servicio|sql\s+injection|sqli|inyeccion(es)?\s+sql|'
                       r'xss|cross-site\s+scripting|rce|ejecucion\s+remota|csrf|phishing|suplantacion|'
                       r'brute\s+force|fuerza\s+bruta|spoofing|mitm|man-in-the-middle|escaner|scanning|'
                       r'deserializacion|deserialization|inseguro(a)?|unsafe|malformed|malformado(a)?|'
            # Caídas, Accesos y Configuraciones Erróneas
                       r'bad\s+request|crash|caida(s)?|bloqueo(s)?|timeout|expiracion|hang|congelamiento|'
                       r'privilege\s+escalation|escalada\s+de\s+privilegios|elevacion\s+de\s+privilegios|'
                       r'root|admin|bypass|evasion|salto\s+de\s+restriccion|auth|autenticacion|'
                       r'broken|roto(a)?|misconfiguration|mala\s+configuracion|configuracion\s+erronea|'
                       r'defecto|default|credential(s)?|credencial(es)?|password(s)?|contraseña(s)?|'
                       r'hardcoded|quemada(s)?|weak|debil|cifrado|encryption|cryptographic|criptografico|'
                       r'directory\s+traversal|salto\s+de\s+directorio|path|ruta|ssrf|lfi|rfi|'
                       r'clickjacking|unauthorized|no\s+autorizado|denegado(a)?'
                       r')\b'),

            # 7. IGNORAR (Separadores de texto y caracteres especiales)
            ('IGNORAR', r'[\s\t\n,.;:()\[\]\{\}\-\"\'\/\\\_\|\<\>\=\+\*\#\&\%\@\?\!\¡\¿]+'),

            # 8. OTROS (Garantía de estabilidad del compilador frente a caracteres residuales)
            ('OTROS', r'.')
        ]
        self.regex_maestro = re.compile('|'.join(f'(?P<{nombre}>{patron})' for nombre, patron in self.reglas_tokens),
                                        re.IGNORECASE)

    def tokenizar(self, texto_reporte):
        """Pipeline Léxico: Convierte la cadena técnica cruda en una secuencia ordenada de tokens normalizados"""
        lista_tokens = []
        for coincidencia in self.regex_maestro.finditer(texto_reporte):
            tipo = coincidencia.lastgroup
            valor = coincidencia.group(tipo)

            if tipo == 'IGNORAR' or tipo == 'OTROS':
                continue

            # Convertimos a mayúsculas y quitamos espacios residuales
            valor_normalizado = valor.upper().strip()

            # TRADUCTOR Y HOMOLOGADOR ACADÉMICO DE SEVERIDADES (Garantiza el mapeo semántico)
            if tipo == 'SEVERIDAD':
                if valor_normalizado in ['CRÍTICO', 'CRÍTICA', 'CRITICO', 'SEVERO', 'SEVERA', 'URGENTE', 'EMERGENCIA']:
                    valor_normalizado = 'CRITICAL'
                elif valor_normalizado in ['ALTO', 'ALTA', 'MODERATE', 'MODERADO', 'MODERADA']:
                    valor_normalizado = 'HIGH'
                elif valor_normalizado in ['MEDIO', 'MEDIA', 'MEDIUM']:
                    valor_normalizado = 'MEDIUM'
                elif valor_normalizado in ['BAJO', 'BAJA', 'LOW', 'INFORMATIVO', 'INFORMATIVA', 'INFO', 'MINIMAL',
                                           'MÍNIMO', 'MÍNIMA', 'ADVISORY']:
                    valor_normalizado = 'LOW'

            lista_tokens.append({
                'tipo': tipo,
                'valor': valor_normalizado if tipo in ['SEVERIDAD'] else valor
            })
        return lista_tokens