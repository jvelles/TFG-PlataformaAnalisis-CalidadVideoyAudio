// Evento para el botón de análisis
document.getElementById('analyze-form').addEventListener('submit', function(e) {
    e.preventDefault();  // Evitar la recarga de página

    const videoUrl = document.getElementById('video-url').value;

    // Llamada a la API de análisis
    fetch('/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ video_url: videoUrl }),
    })
    .then(response => response.json())
    .then(data => {
        mostrarInformacion(data);
        mostrarComentarios(data.comments);
        mostrarGeoPopularidad(data.geo_popularity);
        crearGraficas(data);
    })
    .catch(error => console.error('Error:', error));

    // Mostrar información general del video
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
});


// Mostrar comentarios
function mostrarComentarios(commentsData) {
    const commentsList = document.getElementById('comments-list');
    commentsList.innerHTML = '';

    commentsData.items.forEach(comment => {
        const commentText = comment.snippet.topLevelComment.snippet.textDisplay;
        const li = document.createElement('li');
        li.textContent = commentText;
        commentsList.appendChild(li);
    });
}



