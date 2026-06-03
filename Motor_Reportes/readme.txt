Paso 1:
Antes de empezar asegurense de tener instalado esto con el comando:
pip install -r requirements.txt
el cual tiene las versiones de flask y gunicorn que se esta usando (Flask==3.0.2 gunicorn==21.2.0)

Paso 2:
Si la carpeta .venv no aparece, creala ejecutando el siguiente comando:
python -m venv .venv
el cual sirve para activar el entorno virtual

Paso 3:
Configuración del Módulo de Notificaciones (Gmail)
Para que el botón de alertas por correo funcione correctamente en los entornos locales de cada integrante:
1. Asegurarse de tener conexión estable a internet.
2. Configurar la contraseña de aplicación de Google en la variable `password_emisor` dentro de `backend/output_gen.py`.
3. Levantar el servidor de desarrollo habitual con `python app.py` desde la consola de PowerShell con el entorno (.venv) activo.

IDEAS SIGUIENTE AVANCE

## 🚀 Trabajo Futuro: Pipeline Híbrido de Aprendizaje Continuo (Siguiente Avance)

Para las siguientes fases del proyecto, se implementará un ciclo de retroalimentación continua (Feedback Loop) para mitigar la rigidez de los diccionarios estáticos tradicionales:

1. **Detección de Desconocidos:** Cuando el `lexer.py` identifique componentes residuales (`OTROS`), el sistema no los descartará de forma pasiva.
2. **Consulta Cognitiva a un LLM Local:** Se integrará un modelo de lenguaje de código abierto (ej. Llama 3 / Phi-3 a través de Ollama) de ejecución local gratuita ($0 USD) para interrogar la naturaleza del término desconocido.
3. **Persistencia y Actualización Dinámica:** Las respuestas validadas por la IA se guardarán automáticamente en una base de datos local de conocimiento aumentado (RAG), expandiendo las expresiones regulares del motor en tiempo real para futuras consultas sin dependencias de red.

¿Cómo logramos entonces ese "ciclo sin fin" que imaginaste?
No modificando a la IA, sino utilizando una estrategia de desarrollo llamada RAG (Generación Aumentada por Recuperación) combinada con una base de datos local. El flujo real funciona así:

El usuario ingresa un reporte.

Tu lexer.py detecta un término desconocido.

El sistema le pregunta a la IA: "¿Qué significa este término en ciberseguridad?".

La IA responde: "Es un activo de red".

Tu código de Python escribe ese nuevo término en un archivo de configuración local o base de datos.

En la siguiente consulta, tu lexer.py lee primero esa lista actualizada antes de procesar el texto.