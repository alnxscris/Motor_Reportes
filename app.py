from flask import Flask, render_template, request, jsonify
from backend.lexer import AnalizadorLexicoVulnerabilidades
from backend.parser import AnalizadorSintacticoVulnerabilidades
from backend.semantic import AnalizadorSemanticoVulnerabilidades
from backend.output_gen import GeneradorMitigacion

app = Flask(
    __name__,
    template_folder="frontend/templates",
    static_folder="frontend/static"
)

analizador_lexico = AnalizadorLexicoVulnerabilidades()
analizador_sintactico = AnalizadorSintacticoVulnerabilidades()
analizador_semantico = AnalizadorSemanticoVulnerabilidades()
generador_mitigacion = GeneradorMitigacion()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analizar', methods=['POST'])
def analizar_reporte():
    datos_recibidos = request.get_json()
    texto_crudo = datos_recibidos.get('text', '')

    if not texto_crudo.strip():
        return jsonify({"error": "El reporte enviado no contiene texto para procesar"}), 400

    tokens = analizador_lexico.tokenizar(texto_crudo)
    estructura = analizador_sintactico.analizar_sintaxis(tokens)
    analisis_semantico = analizador_semantico.evaluar_semantica(estructura)
    acciones_mitigacion = generador_mitigacion.generar_acciones_automatizadas(estructura, analisis_semantico)

    return jsonify({
        "tokens": tokens,
        "estructura": estructura,
        "analisis_semantico": analisis_semantico,
        "acciones_mitigacion": acciones_mitigacion
    })


@app.route('/notificar', methods=['POST'])
def notificar_encargado():
    """Recibe los datos del formulario web y ejecuta la acción automatizada mediante el sistema central"""
    try:
        data = request.get_json()

        # Recuperamos solo los datos del incidente
        correo_destino = data.get('correo', '').strip()
        asunto = data.get('asunto', '').strip()
        mensaje = data.get('mensaje', '').strip()

        if not correo_destino or not asunto or not mensaje:
            return jsonify({"status": "error", "message": "Faltan datos del incidente."}), 400

        # Purificación para mantener los caracteres especiales y tildes intactos
        asunto_seguro = asunto.encode('utf-8').decode('utf-8')
        mensaje_seguro = mensaje.encode('utf-8').decode('utf-8')

        # Enviamos las cadenas directas al backend modular
        resultado = generador_mitigacion.enviar_notificacion_gmail(correo_destino, asunto_seguro, mensaje_seguro)
        return jsonify(resultado)

    except Exception as e:
        return jsonify({"status": "error", "message": f"Fallo de orquestación en app.py: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)