// Evento para el botón de análisis
document.getElementById('analyze-form').addEventListener('submit', function(e) {
    e.preventDefault();  // Evitar la recarga de página

    const videoUrl = document.getElementById('video-url').value;

    // Mostrar el loader al iniciar el análisis
    showLoader();

    // Hacer la solicitud de análisis
    fetch('/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ video_url: videoUrl }),
    })
    .then(response => response.json())
    .then(data => {
        console.log("Datos devueltos:", data);  // Verificar respuesta completa en la consola

        // Llamadas a tus funciones para mostrar la información recibida
        mostrarInformacion(data);
        mostrarComentarios(data.comments);
        
        // Mostrar el análisis técnico y de comentarios
        document.getElementById('analysis-result').textContent = data.technical_analysis || 'Análisis técnico no disponible.';
        document.getElementById('comments-analysis-result').textContent = data.comments_analysis || 'Análisis de comentarios no disponible.';

        // Ocultar el loader al terminar el análisis
        hideLoader();
    })
    .catch(error => {
        console.error('Error:', error);
        hideLoader(); // Ocultar el loader en caso de error
    });
});

// Función para mostrar el loader
function showLoader() {
    document.getElementById('loader').style.display = 'flex';
}

// Función para ocultar el loader
function hideLoader() {
    document.getElementById('loader').style.display = 'none';
}

// Funciones para mostrar los resultados de análisis (sin cambios en el contenido original)
function mostrarInformacion(data) {
    const videoInfo = data.video_info.items[0].snippet;
    document.getElementById('video-title').textContent = videoInfo.title;
    document.getElementById('video-published').textContent = videoInfo.publishedAt;
    document.getElementById('video-channel').textContent = videoInfo.channelTitle;
    document.getElementById('video-likes').textContent = data.video_info.items[0].statistics.likeCount || 'No disponible';
    document.getElementById('video-views').textContent = data.video_info.items[0].statistics.viewCount || 'No disponible';

    // Rellenar tabla de análisis de video
    const videoStream = data.video_streams[0];
    document.getElementById('video-analysis').innerHTML = `
        <tr><td>Códec</td><td>${videoStream.codec_name}</td></tr>
        <tr><td>Resolución</td><td>${videoStream.width}x${videoStream.height}</td></tr>
        <tr><td>Bitrate</td><td>${videoStream.bit_rate} bps</td></tr>
        <tr><td>FPS</td><td>${videoStream.avg_frame_rate}</td></tr>
        <tr><td>Formato de Píxeles</td><td>${videoStream.pix_fmt}</td></tr>
        <tr><td>Espacio de Color</td><td>${videoStream.color_space}</td></tr>
        <tr><td>Transferencia de Color</td><td>${videoStream.color_transfer}</td></tr>
        <tr><td>Primarios de Color</td><td>${videoStream.color_primaries}</td></tr>
    `;

    // Rellenar tabla de análisis de audio
    const audioStream = data.audio_streams[0];
    document.getElementById('audio-analysis').innerHTML = `
        <tr><td>Códec</td><td>${audioStream.codec_name}</td></tr>
        <tr><td>Canales</td><td>${audioStream.channels} (${audioStream.channel_layout})</td></tr>
        <tr><td>Bitrate</td><td>${audioStream.bit_rate} bps</td></tr>
        <tr><td>Frecuencia de muestreo</td><td>${audioStream.sample_rate} Hz</td></tr>
        <tr><td>Formato de Muestra</td><td>${audioStream.sample_fmt}</td></tr>
        <tr><td>Frames</td><td>${audioStream.nb_frames}</td></tr>
    `;
}

function mostrarComentarios(comments) {
    const commentsList = document.getElementById('comments-list');
    commentsList.innerHTML = '';  // Limpiar la lista antes de añadir nuevos comentarios

    comments.forEach(commentText => {
        const listItem = document.createElement('li');
        listItem.textContent = commentText;  // Mostrar solo el texto del comentario
        commentsList.appendChild(listItem);
    });
}

// Función para mostrar/ocultar secciones de video y audio
function toggleSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section.style.display === 'none' || section.style.display === '') {
        section.style.display = 'table'; // Muestra la tabla
    } else {
        section.style.display = 'none'; // Oculta la tabla
    }
}