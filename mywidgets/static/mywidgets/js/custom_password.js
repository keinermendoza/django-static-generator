document.addEventListener('DOMContentLoaded', () => {
    const inputContainers = document.getElementsByClassName('custom-password-input-container')
    Array.from(inputContainers).forEach(container => {
        const input =  container.querySelector('.custom-password-input');
        const button =  container.querySelector('.btn-toogle-text');

        button.onclick = () => {
            button.classList.toggle("password-is-visible")
            if (input.type === "password") {
                input.type = "text"
            } else {
                input.type = "password"
            }
        } 

    });
})