import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header


class GeneradorMitigacion:
    def __init__(self):
        # Configuraciones globales de red
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

        # 🔐 CUENTA DE SERVICIO DEL SISTEMA (Credenciales Ocultas e Internas)
        self.correo_sistema = "alaniscris3005@gmail.com"
        self.password_sistema = "hjexfbrajiysyltv"  # Token escrito sin espacios

    def generar_acciones_automatizadas(self, datos_estructurados, resultado_semantico):
        """Genera acciones técnicas automatizadas extrayendo datos de forma dinámica (OE5)"""
        if not resultado_semantico.get("valido", True):
            return [
                "❌ No es posible leer o interpretar ese error.",
                "⚠️ Motivo: El reporte carece de variables de ciberseguridad (IP, puertos, firmas o activos).",
                "💡 Sugerencia: Asegúrese de ingresar una cadena que describa una vulnerabilidad o estado de red simulado."
            ]

        prioridad_actual = resultado_semantico.get("nivel_prioridad", "BAJA")
        lista_acciones = []

        lista_ips = [comp["valor"] for comp in datos_estructurados["componentes_encontrados"] if
                     comp["categoria"] == "Dirección IP"]
        lista_puertos = [comp["valor"] for comp in datos_estructurados["componentes_encontrados"] if
                         comp["categoria"] == "Puerto de Conexión"]
        lista_firmas = [comp["valor"] for comp in datos_estructurados["componentes_encontrados"] if
                        "Firma" in comp["categoria"]]
        lista_activos = [comp["valor"] for comp in datos_estructurados["componentes_encontrados"] if
                         comp["categoria"] == "Componente de Infraestructura"]

        texto_ips = ", ".join(lista_ips) if lista_ips else "red local"
        texto_puertos = ", ".join(lista_puertos) if lista_puertos else "perimetrales"
        texto_firmas = ", ".join(lista_firmas) if lista_firmas else "parche genérico"
        texto_activos = ", ".join(lista_activos) if lista_activos else "sistemas"

        if "ALTA" in prioridad_actual:
            lista_acciones.append(f"ACCIÓN 1: Aislar temporalmente las direcciones IP comprometidas: {texto_ips}.")
            lista_acciones.append(
                f"ACCIÓN 2: Bloquear los puertos de red expuestos: {texto_puertos} en el Firewall perimetral.")
            lista_acciones.append(
                f"ACCIÓN 3: Forzar la descarga e instalación del parche de seguridad para: {texto_firmas}.")
            lista_acciones.append(
                f"ACCIÓN 4: Revocar de forma preventiva las credenciales de administración en los activos: {texto_activos}.")
            lista_acciones.append(
                "ACCIÓN 5: Levantar una alerta roja y disparar el protocolo de contención del equipo de ciberseguridad.")
        elif "24 horas" in prioridad_actual:
            lista_acciones.append(
                f"ACCIÓN 1: Agendar ventana de mantenimiento preventivo urgente en los activos: {texto_activos}.")
            lista_acciones.append(
                f"ACCIÓN 2: Configurar reglas de firmas en el IDS corporativo específicas para mitigar: {texto_firmas}.")
            lista_acciones.append(
                f"ACCIÓN 3: Iniciar un volcado analítico de logs del sistema de las últimas 24 horas sobre las IPs: {texto_ips}.")
            lista_acciones.append(
                "ACCIÓN 4: Enviar correo de notificación de vulnerabilidad en mitigación a los administradores de sistemas.")
            lista_acciones.append(
                f"ACCIÓN 5: Monitorear el tráfico inusual en los puertos: {texto_puertos} para pruebas de regresión.")
        else:
            lista_acciones.append(
                "ACCIÓN 1: Continuar con el monitoreo rutinario y análisis pasivo del tráfico de red.")
            lista_acciones.append(
                f"ACCIÓN 2: Registrar y actualizar el estado de los componentes: {texto_activos} en el inventario.")
            lista_acciones.append(
                "ACCIÓN 3: Almacenar los tokens estructurados en la base de datos de auditoría histórica.")
            lista_acciones.append("ACCIÓN 4: Descartar alerta sonora en el centro de operaciones de seguridad (SOC).")
            lista_acciones.append(
                f"ACCIÓN 5: Programar el escaneo automático estándar para la siguiente ventana semanal.")

        return lista_acciones

    def enviar_notificacion_gmail(self, correo_destino, asunto, mensaje_texto):
        """
        Envía un correo electrónico automatizado utilizando el SMTP de Gmail.
        Utiliza de manera automática las credenciales del sistema central.
        """
        try:
            msg = MIMEMultipart()

            # Formateo seguro para la red usando el correo del SISTEMA
            msg['From'] = Header(self.correo_sistema, 'utf-8')
            msg['To'] = Header(correo_destino, 'utf-8')
            msg['Subject'] = Header(asunto, 'utf-8')

            msg.attach(MIMEText(mensaje_texto, 'plain', 'utf-8'))

            # Negociación del túnel TLS seguro
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()

            # 🌟 AUTENTICACIÓN INVISIBLE: Inicia sesión usando tus datos guardados arriba
            server.login(self.correo_sistema, self.password_sistema)

            server.sendmail(self.correo_sistema, correo_destino, msg.as_bytes())
            server.quit()

            return {"status": "success", "message": "Notificación enviada con éxito al encargado de TI."}
        except Exception as e:
            return {"status": "error", "message": f"Error interno de envío: {str(e)}"}