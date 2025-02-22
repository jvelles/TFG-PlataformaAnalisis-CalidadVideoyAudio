// 1. Evento para el botón de análisis

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
    .then(response => {
        if (!response.ok) {
            return response.json().then(errorData => {
                showModal(errorData.error); // Mostrar modal personalizado
                throw new Error(errorData.error);
            });
        }
        return response.json();
    })
    .then(data => {
        console.log("Datos devueltos:", data); 
        mostrarInformacion(data);
        mostrarComentarios(data.comments);
        mostrarAnalisisTecnico(data.technical_analysis);
        mostrarAnalisisDeComentarios(data.comments_analysis);

        // Ocultar el loader al terminar el análisis
        hideLoader();
    })
    .catch(error => {
        console.error('Error:', error);
        hideLoader(); 
    });
});

// 2. Funciones para manejar el loader

function showLoader() {
    document.getElementById('loader').style.display = 'flex';
}

function hideLoader() {
    document.getElementById('loader').style.display = 'none';
}

// 3. Función para mostrar información del video

function mostrarInformacion(data) {
    const videoInfo = data.video_info.items[0].snippet;
// Convertir la fecha a un formato legible
    const rawDate = videoInfo.publishedAt; 
    let formattedDate = "Fecha no disponible";
    
    const dateMatch = rawDate.match(/^(\d{4})-(\d{2})-(\d{2})/); // Extraer año, mes y día
    if (dateMatch) {
        const year = dateMatch[1];
        const month = parseInt(dateMatch[2], 10); 
        const day = dateMatch[3];    
        const monthNames = [
            "enero", "febrero", "marzo", "abril", "mayo", "junio",
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
        ];
        formattedDate = `${day} de ${monthNames[month - 1]} de ${year}`;
    }
    
    
    document.getElementById('video-title').textContent = videoInfo.title;
    document.getElementById('video-published').textContent = formattedDate;
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

// 4. Función para mostrar comentarios

function mostrarComentarios(comments) {
    const commentsList = document.getElementById('comments-list');
    commentsList.innerHTML = '';  // Limpiar la lista antes de añadir nuevos comentarios

    comments.forEach(commentText => {
        const listItem = document.createElement('li');
        listItem.textContent = commentText;  // Mostrar solo el texto del comentario
        commentsList.appendChild(listItem);
    });
}

// 5. Función para alternar la visibilidad de secciones

function toggleSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section.style.display === 'none' || section.style.display === '') {
        section.style.display = 'table'; // Muestra la tabla
    } else {
        section.style.display = 'none'; // Oculta la tabla
    }
}

// 6. Función para dividir el texto en párrafos

function formatTextAsParagraphs(text) {
    const sentences = text.split('. ');
    return sentences.map(sentence => `<p>${sentence.trim()}.</p>`).join('');
}

// 7. Función para mostrar análisis técnico

function mostrarAnalisisTecnico(technicalAnalysis) {
    const container = document.getElementById('analysis-result');
    container.innerHTML = ''; 

    // Dividir el análisis en párrafos
    const paragraphs = technicalAnalysis.split('. '); // Dividir por puntos
    paragraphs.forEach(paragraph => {
        if (paragraph.trim()) { // Asegurarse de no añadir párrafos vacíos
            const p = document.createElement('p');
            // Verificar y limpiar el punto al final
            const cleanedParagraph = paragraph.trim().replace(/\.+$/, ''); 
            p.textContent = cleanedParagraph + '.'; 
            container.appendChild(p); // Agregar cada párrafo al contenedor
        }
    });
}

// 8. Función para mostrar análisis de comentarios

function mostrarAnalisisDeComentarios(commentsAnalysis) {
    const container = document.getElementById('comments-analysis-result');
    container.innerHTML = ''; // Limpiar contenido previo

    // Dividir el análisis en párrafos
    const paragraphs = commentsAnalysis.split('. '); // Dividir por puntos
    paragraphs.forEach(paragraph => {
        if (paragraph.trim()) { // Asegurar de no añadir párrafos vacíos
            const p = document.createElement('p');
            // Verificar y limpiar el punto al final
            const cleanedParagraph = paragraph.trim().replace(/\.+$/, ''); 
            p.textContent = cleanedParagraph + '.'; 
            container.appendChild(p); // Agregar cada párrafo al contenedor
        }
    });
}

// 9. Evento para alternar modo oscuro

const toggleButton = document.getElementById('dark-mode-toggle');
document.addEventListener('DOMContentLoaded', () => {
    if (localStorage.getItem('darkMode') === 'enabled') {
        document.body.classList.add('dark-mode');
        if (toggleButton) {
            toggleButton.textContent = '☀️ Modo Claro';
        }
    }
});
if (toggleButton) {
    toggleButton.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        
        if (document.body.classList.contains('dark-mode')) {
            localStorage.setItem('darkMode', 'enabled');
            toggleButton.textContent = '☀️ Modo Claro';
        } else {
            localStorage.setItem('darkMode', 'disabled');
            toggleButton.textContent = '🌙 Modo Oscuro';
        }
    });
}

// 10. Función para mostrar el modal de error personalizado

function showModal(message) {
    const modal = document.getElementById('errorModal');
    const modalMessage = document.getElementById('modal-message');
    modalMessage.textContent = message;
    modal.style.display = "flex";

    // Cerrar modal al hacer clic en la "X" o el botón Aceptar
    document.querySelector('.close').onclick = function() {
        modal.style.display = "none";
    };

    document.getElementById('modal-ok-btn').onclick = function() {
        modal.style.display = "none";
    };

    // Cerrar al hacer clic fuera del modal
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };
}


