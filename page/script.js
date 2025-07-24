/**
 * Aplicación web para interactuar con API de K-Means
 * Permite hacer peticiones GET y POST, mostrando los resultados en formato JSON
 */

// Variables globales
const API_BASE_URL = 'http://127.0.0.1:8000';

// DOM Elements
const elements = {
    postUrlInput: document.getElementById('kmeansPostUrl'),
    postDataInput: document.getElementById('kmeansPostData'),
    getUrlInput: document.getElementById('kmeansGetUrl'),
    postButton: document.getElementById('buttonTextKmeansPost'),
    getButton: document.getElementById('buttonTextKmeansGet'),
    postSpinner: document.getElementById('loadingSpinnerKmeansPost'),
    getSpinner: document.getElementById('loadingSpinnerKmeansGet'),
    statusDiv: document.getElementById('status'),
    errorDiv: document.getElementById('error'),
    resultsContainer: document.getElementById('predictionsContainer')
};

// Inicialización
document.addEventListener('DOMContentLoaded', () => {
    // Set default URLs
    elements.postUrlInput.value = `${API_BASE_URL}/kmeans/guardar`;
    elements.getUrlInput.value = `${API_BASE_URL}/kmeans/clusterizados`;
    
    // Set default POST data
    elements.postDataInput.value = JSON.stringify({
        venta_id: 1490,
        hora: 18,
        dia_semana: 5,
        id_producto: 14,
        cantidad: 3,
        precio_total: 15
    }, null, 2);
});

// ==================== FUNCIONES PRINCIPALES ====================

/**
 * Guarda datos mediante POST a /kmeans/guardar
 */
async function guardarDatosKmeans() {
    const apiUrl = elements.postUrlInput.value;
    const postDataText = elements.postDataInput.value;
    
    // Validaciones
    if (!validarUrl(apiUrl)) {
        mostrarError('Por favor ingresa una URL válida para el endpoint POST');
        return;
    }
    
    let postData;
    try {
        postData = JSON.parse(postDataText);
    } catch (e) {
        mostrarError('Los datos para POST deben estar en formato JSON válido');
        return;
    }
    
    if (!validarDatosVenta(postData)) {
        return;
    }
    
    // Configurar UI para carga
    toggleLoading(true, 'post');
    
    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(postData)
        });
        
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Mostrar resultados
        mostrarResultados(data, `✅ Datos guardados exitosamente (${response.status} ${response.statusText})`);
        
    } catch (error) {
        mostrarError(`Error al guardar datos: ${error.message}`);
        console.error('Error detallado:', error);
    } finally {
        toggleLoading(false, 'post');
    }
}

/**
 * Obtiene resultados mediante GET a /kmeans/clusterizados
 */
async function obtenerResultadosKmeans() {
    const apiUrl = elements.getUrlInput.value;
    
    // Validaciones
    if (!validarUrl(apiUrl)) {
        mostrarError('Por favor ingresa una URL válida para el endpoint GET');
        return;
    }
    
    // Configurar UI para carga
    toggleLoading(true, 'get');
    
    try {
        const response = await fetch(apiUrl, {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Mostrar resultados
        mostrarResultados(data, `✅ Datos obtenidos exitosamente (${response.status} ${response.statusText})`);
        
    } catch (error) {
        mostrarError(`Error al obtener datos: ${error.message}`);
        console.error('Error detallado:', error);
    } finally {
        toggleLoading(false, 'get');
    }
}

// ==================== FUNCIONES DE UTILIDAD ====================

/**
 * Muestra los resultados en el contenedor
 */
function mostrarResultados(data, statusMessage = '') {
    // Limpiar contenedores
    elements.resultsContainer.innerHTML = '';
    
    // Mostrar mensaje de estado si existe
    if (statusMessage) {
        mostrarStatus(statusMessage);
    }
    
    // Crear sección para el JSON crudo
    const jsonSection = document.createElement('div');
    jsonSection.className = 'response-section';
    
    const jsonTitle = document.createElement('h3');
    jsonTitle.textContent = 'Respuesta JSON Completa';
    jsonSection.appendChild(jsonTitle);
    
    const jsonPre = document.createElement('pre');
    jsonPre.className = 'json-response';
    jsonPre.textContent = JSON.stringify(data, null, 2);
    jsonSection.appendChild(jsonPre);
    
    elements.resultsContainer.appendChild(jsonSection);
    
    // Si los datos tienen estructura de cluster, mostrar vista especial
    if (data.resultados && Array.isArray(data.resultados) && data.resultados.some(item => 'cluster' in item)) {
        mostrarVistaCluster(data.resultados);
    }
    
    // Mostrar en consola para depuración
    console.log('Datos recibidos:', data);
}

/**
 * Muestra una vista especial para datos clusterizados
 */
function mostrarVistaCluster(resultados) {
    const clusterSection = document.createElement('div');
    clusterSection.className = 'response-section';
    
    const clusterTitle = document.createElement('h3');
    clusterTitle.textContent = 'Vista de Clusters';
    clusterSection.appendChild(clusterTitle);
    
    // Agrupar por cluster
    const clusters = {};
    resultados.forEach(item => {
        const clusterId = item.cluster || 0;
        if (!clusters[clusterId]) {
            clusters[clusterId] = {
                items: [],
                descripcion: item.descripcion || `Cluster ${clusterId}`
            };
        }
        clusters[clusterId].items.push(item);
    });
    
    // Crear tarjetas para cada cluster
    Object.entries(clusters).forEach(([clusterId, clusterData]) => {
        const clusterCard = document.createElement('div');
        clusterCard.className = 'cluster-card';
        
        const clusterHeader = document.createElement('div');
        clusterHeader.className = `cluster-header cluster-${clusterId % 3}`;
        clusterHeader.textContent = `${clusterData.descripcion} (${clusterData.items.length} elementos)`;
        clusterCard.appendChild(clusterHeader);
        
        // Crear tabla para los items del cluster
        const table = document.createElement('table');
        
        // Cabecera de tabla
        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');
        ['Venta ID', 'Hora', 'Día', 'Producto', 'Cantidad', 'Total'].forEach(text => {
            const th = document.createElement('th');
            th.textContent = text;
            headerRow.appendChild(th);
        });
        thead.appendChild(headerRow);
        table.appendChild(thead);
        
        // Cuerpo de tabla
        const tbody = document.createElement('tbody');
        clusterData.items.forEach(item => {
            const row = document.createElement('tr');
            
            [item.venta_id || 'N/A', 
             item.hora ? `${item.hora}:00` : 'N/A', 
             obtenerNombreDia(item.dia_semana), 
             item.id_producto || 'N/A', 
             item.cantidad || 'N/A', 
             item.precio_total ? `$${item.precio_total.toFixed(2)}` : 'N/A'
            ].forEach(text => {
                const td = document.createElement('td');
                td.textContent = text;
                row.appendChild(td);
            });
            
            tbody.appendChild(row);
        });
        table.appendChild(tbody);
        
        clusterCard.appendChild(table);
        clusterSection.appendChild(clusterCard);
    });
    
    elements.resultsContainer.insertBefore(clusterSection, elements.resultsContainer.firstChild);
}

/**
 * Muestra un mensaje de estado
 */
function mostrarStatus(mensaje) {
    elements.statusDiv.textContent = mensaje;
    elements.statusDiv.style.display = 'block';
    elements.statusDiv.style.backgroundColor = '#d4edda';
    elements.statusDiv.style.color = '#155724';
}

/**
 * Muestra un mensaje de error
 */
function mostrarError(mensaje) {
    elements.errorDiv.textContent = mensaje;
    elements.errorDiv.style.display = 'block';
    elements.statusDiv.style.display = 'none';
}

/**
 * Limpia los resultados y mensajes
 */
function limpiarResultados() {
    elements.resultsContainer.innerHTML = '';
    elements.statusDiv.style.display = 'none';
    elements.errorDiv.style.display = 'none';
}

/**
 * Controla el estado de carga
 */
function toggleLoading(loading, type) {
    if (type === 'post') {
        elements.postSpinner.style.display = loading ? 'inline-block' : 'none';
        elements.postButton.textContent = loading ? 'Guardando...' : 'Guardar Datos (POST)';
    } else {
        elements.getSpinner.style.display = loading ? 'inline-block' : 'none';
        elements.getButton.textContent = loading ? 'Cargando...' : 'Obtener Resultados (GET)';
    }
}

/**
 * Valida una URL
 */
function validarUrl(url) {
    try {
        new URL(url);
        return true;
    } catch {
        return false;
    }
}

/**
 * Valida los datos de venta para POST
 */
function validarDatosVenta(data) {
    const requiredFields = [
        'venta_id', 'hora', 'dia_semana', 
        'id_producto', 'cantidad', 'precio_total'
    ];
    
    const missingFields = requiredFields.filter(field => !(field in data));
    
    if (missingFields.length > 0) {
        mostrarError(`Faltan campos requeridos: ${missingFields.join(', ')}`);
        return false;
    }
    
    return true;
}

/**
 * Convierte número de día a nombre
 */
function obtenerNombreDia(numeroDia) {
    const dias = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
    return dias[numeroDia] || `Día ${numeroDia}`;
}

// ==================== EVENT LISTENERS ====================

// Enter en campo de URL GET
elements.getUrlInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        obtenerResultadosKmeans();
    }
});

// Ctrl+Enter en campo de datos POST
elements.postDataInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && e.ctrlKey) {
        guardarDatosKmeans();
    }
});