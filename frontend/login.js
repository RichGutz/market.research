document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const errorMessage = document.getElementById('errorMessage');

    // Limpiar sesión anterior
    sessionStorage.removeItem('gyp_authenticated');

    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const username = usernameInput.value.trim().toLowerCase();
        const password = passwordInput.value;

        // Hardcoded credentials according to user request
        if (username === 'rgutil@gmail.com' && password === 'VivaLaVida2026$') {
            // Éxito
            sessionStorage.setItem('gyp_authenticated', 'true');
            sessionStorage.setItem('gyp_user', username);
            window.location.href = 'gyp.html';
        } else {
            // Fallo
            errorMessage.textContent = 'Credenciales incorrectas o usuario no autorizado.';
            
            // Animación de error
            loginForm.animate([
                { transform: 'translateX(0)' },
                { transform: 'translateX(-10px)' },
                { transform: 'translateX(10px)' },
                { transform: 'translateX(-10px)' },
                { transform: 'translateX(10px)' },
                { transform: 'translateX(0)' }
            ], {
                duration: 400,
                iterations: 1
            });
        }
    });
});
