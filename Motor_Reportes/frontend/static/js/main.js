async function procesarMotor() {
    const textoReporte = document.getElementById("txtReporte").value;
    const botonProcesar = document.getElementById("btnProcesar");

    if (!textoReporte.trim()) {
        alert("Por favor, introduce un reporte técnico para ser procesado por el motor.");
        return;
    }

    botonProcesar.textContent = "Procesando Pipeline Técnico...";
    botonProcesar.disabled = true;

    try {
        const respuesta = await fetch('/analizar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: textoReporte })
        });

        if (!respuesta.ok) throw new Error("Fallo crítico en el procesamiento del servidor backend.");

        const resultado = await respuesta.json();

        // REFORMA FASE 1: Renderizado de Etiquetas (Tokens)
        const contenedorEtiquetas = document.getElementById("outLexer");
        contenedorEtiquetas.innerHTML = "";

        if (resultado.tokens.length === 0) {
            contenedorEtiquetas.innerHTML = '<span class="placeholder-texto">No se identificaron componentes clave.</span>';
        } else {
            resultado.tokens.forEach(token => {
                const spanBadge = document.createElement("span");
                spanBadge.className = `badge-token ${token.tipo}`;
                spanBadge.textContent = `${token.tipo}: ${token.valor}`;
                contenedorEtiquetas.appendChild(spanBadge);
            });
        }

        // REFORMA FASE 2: Tabla Completamente Dinámica y Adaptativa
        const contenedorTabla = document.getElementById("outParser");
        const estructuraSintactica = resultado.estructura;

        if (!estructuraSintactica.tiene_datos_validos) {
            contenedorTabla.innerHTML = '<span class="placeholder-texto">No hay datos estructurados disponibles para esta entrada.</span>';
        } else {
            let filasComponentesHTML = "";
            estructuraSintactica.componentes_encontrados.forEach(item => {
                filasComponentesHTML += `
                    <tr>
                        <td><strong>${item.categoria}</strong></td>
                        <td style="color: #38bdf8; font-family: monospace;">${item.valor}</td>
                    </tr>
                `;
            });

            let filasRelacionesHTML = "";
            if (estructuraSintactica.relaciones_contextuales.length === 0) {
                filasRelacionesHTML = `
                    <tr>
                        <td><strong style="color: #64748b;">Deducción Gramatical</strong></td>
                        <td style="color: #64748b; font-style: italic;">Componentes aislados. No se detectaron patrones secuenciales complejos.</td>
                    </tr>
                `;
            } else {
                estructuraSintactica.relaciones_contextuales.forEach(relacion => {
                    filasRelacionesHTML += `
                        <tr>
                            <td><strong style="color: #f59e0b;"> ${relacion.tipo_relacion}</strong></td>
                            <td style="color: #e2e8f0;">${relacion.descripcion}</td>
                        </tr>
                    `;
                });
            }

            contenedorTabla.innerHTML = `
                <table class="tabla-sintactica">
                    <thead>
                        <tr>
                            <th style="width: 35%;">Propiedad Gramatical</th>
                            <th>Mapeo de Datos Extraídos en Tiempo Real</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${filasComponentesHTML}
                        ${filasRelacionesHTML}
                    </tbody>
                </table>
            `;
        }

        // RENDERIZADO DE LAS FASES SEMÁNTICA Y SALIDA AUTOMATIZADA
        document.getElementById("lblRiesgo").textContent = resultado.analisis_semantico.nivel_riesgo;
        document.getElementById("lblPrioridad").textContent = resultado.analisis_semantico.nivel_prioridad;
        document.getElementById("lblRegla").textContent = resultado.analisis_semantico.regla_aplicada;

        const contenedorLista = document.getElementById("listAcciones");
        contenedorLista.innerHTML = "";

        resultado.acciones_mitigacion.forEach(accion => {
            const elementoLi = document.createElement("li");
            elementoLi.textContent = accion;
            contenedorLista.appendChild(elementoLi);
        });

    } catch (error) {
        console.error(error);
        alert("Ocurrió un error al intentar conectarse con el servidor Flask.");
    } finally {
        botonProcesar.textContent = "Compilar y Procesar Reporte";
        botonProcesar.disabled = false;
    }
}

// ======================================================================
// ENLACE INTERACTIVO: ENVÍO DE CORREO AUTOMATIZADO POR EL SISTEMA
// ======================================================================
document.getElementById("btnNotificar").addEventListener("click", async () => {
    // Solo capturamos información del incidente, el usuario final no hace login
    const correo = document.getElementById("email_ti").value;
    const asunto = document.getElementById("asunto_ti").value;
    const mensaje = document.getElementById("mensaje_ti").value;
    const statusTxt = document.getElementById("status_notificacion");

    if (!correo.trim() || !asunto.trim() || !mensaje.trim()) {
        statusTxt.style.color = "#ef4444";
        statusTxt.innerText = "Por favor, completa el destinatario, asunto y mensaje del reporte.";
        return;
    }

    statusTxt.style.color = "#38bdf8";
    statusTxt.innerText = "El Servidor Central está enviando la alerta segura...";

    try {
        const response = await fetch("/notificar", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ correo, asunto, mensaje })
        });

        const data = await response.json();

        if (data.status === "success") {
            statusTxt.style.color = "#10b981";
            statusTxt.innerText = "¡Notificación enviada con éxito desde el Servidor Central!";
        } else {
            statusTxt.style.color = "#ef4444";
            statusTxt.innerText = "Error del Sistema: " + data.message;
        }
    } catch (error) {
        console.error(error);
        statusTxt.style.color = "#ef4444";
        statusTxt.innerText = "No se pudo establecer comunicación con el servidor de notificaciones.";
    }
});