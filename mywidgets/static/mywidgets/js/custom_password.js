document.addEventListener('DOMContentLoaded', () => {
    const inputContainers = document.getElementsByClassName('custom-password-input-container')
    Array.from(inputContainers).forEach(container => {
        const input =  container.querySelector('.custom-password-input');
        const button =  container.querySelector('.btn-toogle-text');
        const svgShow = container.querySelector('.pasword-hidden');
        const svgHide = container.querySelector('.password-showed');
        
        // hide svg on init
        svgHide.style.display = "none";
        button.style.display = "grid";

        button.onclick = () => {
            button.classList.toggle("password-is-visible")
            if (input.type === "password") {
                input.type = "text"

                svgShow.style.display = "none";
                svgHide.style.display = "block";

            } else {
                svgShow.style.display = "block";
                svgHide.style.display = "none";

                input.type = "password"
            }
        } 

    });
})