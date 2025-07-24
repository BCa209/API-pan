// Variable global para controlar el estado de carga
let isLoading = false;

/**
 * Función principal para obtener resultados del análisis Apriori
 */
async function obtenerResultadosApriori() {
    if (isLoading) return;
    
    let apiUrl = document.getElementById('apiUrl').value.trim();
    
    // Si la URL es relativa o localhost, usar la misma base que la página actual
    if (apiUrl.includes('localhost') || apiUrl.includes('127.0.0.1')) {
        // Usar la misma IP/puerto que está sirviendo la página
        const currentHost = window.location.hostname;
        const currentProtocol = window.location.protocol;
        apiUrl = apiUrl.replace(/https?:\/\/(localhost|127\.0\.0\.1)/, `${currentProtocol}//${currentHost}`);
    }
    
    const button = document.querySelector('button');
    const buttonText = document.getElementById('buttonText');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const resultsDiv = document.getElementById('results');
    const errorDiv = document.getElementById('error');
    const statusDiv = document.getElementById('status');

    // Validar URL
    if (!apiUrl) {
        mostrarError('Por favor, ingresa una URL válida');
        return;
    }

    // Mostrar estado de carga
    mostrarEstadoCarga(true, button, buttonText, loadingSpinner);
    
    // Ocultar resultados y errores previos
    ocultarElementosPrevios(resultsDiv, errorDiv, statusDiv);

    try {
        mostrarStatus('Enviando petición...', 'success');
        
        console.log(`Intentando conectar a: ${apiUrl}`);
        
        const response = await fetch(apiUrl, {
            method: 'GET',
            mode: 'cors',
            cache: 'no-cache'
        });

        console.log('Respuesta recibida. Status:', response.status);

        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status} - ${response.statusText}`);
        }

        const data = await response.json();
        console.log('Datos parseados:', data);

        // Verificar que la respuesta tenga el formato esperado
        if (data && data.reglas && Array.isArray(data.reglas)) {
            mostrarResultadosApriori(data);
            mostrarStatus(`✅ Se obtuvieron ${data.reglas.length} reglas de asociación`, 'success');
        } else {
            throw new Error('La respuesta no tiene el formato esperado. Se esperaba: {"reglas": [array], ...}');
        }

    } catch (error) {
        console.error('Error completo:', error);
        
        let mensajeError = 'Error desconocido';
        
        if (error.message.includes('Failed to fetch')) {
            mensajeError = 'No se puede conectar al servidor. Verifica que tu API esté corriendo en la URL especificada.';
        } else if (error.message.includes('NetworkError')) {
            mensajeError = 'Error de red. Verifica tu conexión a internet y que el servidor esté disponible.';
        } else if (error.message.includes('CORS')) {
            mensajeError = 'Error de CORS. El servidor debe permitir peticiones desde este origen.';
        } else {
            mensajeError = error.message;
        }
        
        mostrarError(`Error: ${mensajeError}`);
        mostrarStatus('❌ Error en la petición', 'error');
    } finally {
        mostrarEstadoCarga(false, button, buttonText, loadingSpinner);
    }
}

/**
 * Muestra los resultados del análisis Apriori en la interfaz
 * @param {Object} data - Datos del análisis Apriori
 */
function mostrarResultadosApriori(data) {
    const resultsDiv = document.getElementById('results');
    const predictionsContainer = document.getElementById('predictionsContainer');
    
    // Limpiar contenido anterior
    predictionsContainer.innerHTML = '';
    
    // Crear elementos para mostrar la información general
    const infoDiv = document.createElement('div');
    infoDiv.className = 'info-general';
    infoDiv.innerHTML = `
        <h3>📊 Análisis de Reglas de Asociación</h3>
        <p><strong>Fecha de análisis:</strong> ${data.fecha_analisis}</p>
        <p><strong>Periodo:</strong> ${data.periodo}</p>
        <p><strong>Total de transacciones:</strong> ${data.total_transacciones}</p>
        <h4>Reglas encontradas (${data.reglas.length}):</h4>
    `;
    predictionsContainer.appendChild(infoDiv);
    
    // Crear elementos para cada regla
    data.reglas.forEach((regla, index) => {
        const reglaDiv = document.createElement('div');
        reglaDiv.className = 'regla-item';
        reglaDiv.innerHTML = `
            <div class="regla-header">
                <span>Regla ${index + 1}:</span>
                <span class="regla-soporte">Soporte: ${(regla.support * 100).toFixed(2)}%</span>
            </div>
            <div class="regla-body">
                <p>Si se compra <strong>${regla.antecedents.join(', ')}</strong>, entonces también se compra <strong>${regla.consequents.join(', ')}</strong></p>
                <div class="regla-metrics">
                    <span>Confianza: ${(regla.confidence * 100).toFixed(2)}%</span>
                    <span>Lift: ${regla.lift.toFixed(2)}</span>
                </div>
            </div>
        `;
        predictionsContainer.appendChild(reglaDiv);
    });
    
    // Mostrar resultados con animación
    setTimeout(() => {
        resultsDiv.classList.add('show');
    }, 100);
}

/**
 * Muestra el estado de la petición
 * @param {string} mensaje - Mensaje de estado
 * @param {string} tipo - Tipo de estado ('success' o 'error')
 */
function mostrarStatus(mensaje, tipo) {
    const statusDiv = document.getElementById('status');
    statusDiv.textContent = mensaje;
    statusDiv.className = `status ${tipo}`;
    statusDiv.style.display = 'block';
}

/**
 * Prueba la conexión al servidor sin hacer la petición completa
 */
async function probarConexion() {
    const apiUrl = document.getElementById('apiUrl').value.trim();
    
    if (!apiUrl) {
        mostrarError('Por favor, ingresa una URL válida');
        return;
    }

    mostrarStatus('Probando conexión...', 'success');
    
    try {
        // Extraer la URL base (sin el endpoint específico)
        const urlBase = apiUrl.replace('/predecir-todos', '');
        
        const response = await fetch(urlBase, {
            method: 'GET',
            mode: 'no-cors' // Esto evita errores CORS para la prueba
        });
        
        mostrarStatus('✅ Conexión exitosa al servidor', 'success');
        console.log('Servidor alcanzable en:', urlBase);
        
    } catch (error) {
        console.error('Error de conexión:', error);
        mostrarStatus('❌ No se puede conectar al servidor', 'error');
        mostrarError(`Error de conexión: ${error.message}`);
    }
}

/**
 * Limpia todos los resultados y mensajes
 */
function limpiarResultados() {
    document.getElementById('results').classList.remove('show');
    document.getElementById('error').style.display = 'none';
    document.getElementById('status').style.display = 'none';
}/*
 * @param {boolean} cargando - Si está cargando o no
 * @param {HTMLElement} button - Elemento del botón
 * @param {HTMLElement} buttonText - Texto del botón
 * @param {HTMLElement} loadingSpinner - Spinner de carga
 */
function mostrarEstadoCarga(cargando, button, buttonText, loadingSpinner) {
    isLoading = cargando;
    button.disabled = cargando;
    
    if (cargando) {
        buttonText.style.display = 'none';
        loadingSpinner.style.display = 'inline-block';
    } else {
        buttonText.style.display = 'inline';
        loadingSpinner.style.display = 'none';
    }
}

/**
 * Oculta elementos previos antes de mostrar nuevos resultados
 * @param {HTMLElement} resultsDiv - Div de resultados
 * @param {HTMLElement} errorDiv - Div de errores
 * @param {HTMLElement} statusDiv - Div de estado
 */
function ocultarElementosPrevios(resultsDiv, errorDiv, statusDiv) {
    resultsDiv.classList.remove('show');
    errorDiv.style.display = 'none';
    statusDiv.style.display = 'none';
}

/**
 * Valida si una URL tiene un formato básico válido
 * @param {string} url - URL a validar
 * @returns {boolean} - True si es válida
 */
function validarURL(url) {
    try {
        new URL(url);
        return true;
    } catch {
        return false;
    }
}

// Modifica el event listener para usar la nueva función
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('apiUrl').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            obtenerResultadosApriori();
        }
    });

    console.log('Cliente de análisis Apriori cargado. Listo para hacer peticiones GET.');
    
    document.getElementById('apiUrl').addEventListener('input', function(e) {
        const url = e.target.value.trim();
        if (url && !validarURL(url)) {
            e.target.style.borderColor = '#e74c3c';
        } else {
            e.target.style.borderColor = '#e1e5e9';
        }
    });
});