function togglePasswordVisibility(passwordId, event) {
        const passwordInput = document.getElementById(passwordId);
        const parentSpan = event.currentTarget;
        const eyeOpen = parentSpan.querySelector('.eye-icon-open');
        const eyeSlash = parentSpan.querySelector('.eye-icon-slash');
        
        const isPassword = passwordInput.getAttribute('type') === 'password';
        
        if (isPassword) {
            passwordInput.setAttribute('type', 'text');
            eyeOpen.classList.add('hidden');
            eyeSlash.classList.remove('hidden');
        } else {
            passwordInput.setAttribute('type', 'password');
            eyeOpen.classList.remove('hidden');
            eyeSlash.classList.add('hidden');
        }
    }