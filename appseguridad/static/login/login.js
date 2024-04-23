/* console.log('Hello word')

const video = document.getElementById('video-element')

if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({video:true})
    .then((stream)=>{
        video.srcObject =stream
    })
}  */

 const video = document.getElementById('video-element');
        
        // Verificar si el navegador admite la API de medios web
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            // Acceder a la cámara
            navigator.mediaDevices.getUserMedia({ video: true })
                .then(function (stream) {
                    video.srcObject = stream;
                })
                .catch(function (error) {
                    console.error('Error al acceder a la cámara:', error);
                });
        } else {
            console.error('Tu navegador no admite la API de medios web');
        } 