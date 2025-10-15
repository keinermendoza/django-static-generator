const messagesElement = document.getElementById("django-messages");

if (messagesElement) {
    const messages = JSON.parse(messagesElement.textContent || '[]');
    const durationMs = 5000; 

    const Toast = Swal.mixin({
        toast: true,                  // activa el modo toast
        position: 'top-end',          // posición: top-start, top-end, bottom-start, bottom-end
        showConfirmButton: false,     // sin botón de confirmación
        timer: durationMs,                  // se cierra automáticamente en 3s
        timerProgressBar: true,       // muestra barra de progreso
        didOpen: (toast) => {
        toast.addEventListener('mouseenter', Swal.stopTimer)
        toast.addEventListener('mouseleave', Swal.resumeTimer)
        }
    })
    
    messages.forEach((message, index) => {
        const icon = message.level === 'error' ? 'error' :
                message.level === 'warning' ? 'warning' :
                message.level === 'info' ? 'info' : 'success';
        setTimeout(() => {
            Toast.fire({
                icon: icon,
                title: message.message
            })
        }, index * durationMs)
    });

}


