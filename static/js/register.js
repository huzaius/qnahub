

    .modern - form {
    --primary: #3b82f6;
    --primary - dark: #2563eb;
    --primary - light: rgba(59, 130, 246, 0.1);
    --success: #10b981;
    --text - main: #1e293b;
    --text - secondary: #64748b;
    --bg - input: #f8fafc;

    position: relative;
    width: 300px;
    padding: 24px;
    margin: 50px auto;
    background: #ffffff;
    border - radius: 16px;
    box - shadow:
    0 4px 6px - 1px rgba(0, 0, 0, 0.1),
        0 2px 4px - 2px rgba(0, 0, 0, 0.05),
            inset 0 0 0 1px rgba(148, 163, 184, 0.1);
    font - family: system - ui, -apple - system, sans - serif;
}

    .form - title {
    font - size: 22px;
    font - weight: 600;
    color: var(--text - main);
    margin: 0 0 24px;
    text - align: center;
    letter - spacing: -0.01em;
}

    .input - group {
    margin - bottom: 16px;
}

    .input - wrapper {
    position: relative;
    display: flex;
    align - items: center;
}

    .form - input {
    width: 100 %;
    height: 40px;
    padding: 0 36px;
    font - size: 14px;
    border: 1px solid #e2e8f0;
    border - radius: 10px;
    background: var(--bg - input);
    color: var(--text - main);
    transition: all 0.2s ease;
}

    .form - input::placeholder {
    color: var(--text - secondary);
}

    .input - icon {
    position: absolute;
    left: 12px;
    width: 16px;
    height: 16px;
    color: var(--text - secondary);
    pointer - events: none;
}

    .password - toggle {
    position: absolute;
    right: 12px;
    display: flex;
    align - items: center;
    padding: 4px;
    background: none;
    border: none;
    color: var(--text - secondary);
    cursor: pointer;
    transition: all 0.2s ease;
}

    .eye - icon {
    width: 16px;
    height: 16px;
}

    .submit - button {
    position: relative;
    width: 100 %;
    height: 40px;
    margin - top: 8px;
    background: var(--primary);
    color: white;
    border: none;
    border - radius: 10px;
    font - size: 14px;
    font - weight: 500;
    cursor: pointer;
    overflow: hidden;
    transition: all 0.2s ease;
}

    .button - glow {
    position: absolute;
    inset: 0;
    background: linear - gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    transform: translateX(-100 %);
    transition: transform 0.5s ease;
}

    .form - footer {
    margin - top: 16px;
    text - align: center;
    font - size: 13px;
}

    .login - link {
    color: var(--text - secondary);
    text - decoration: none;
    transition: all 0.2s ease;
}

    .login - link span {
    color: var(--primary);
    font - weight: 500;
}

    .form - input:hover {
    border - color: #cbd5e1;
}

    .form - input:focus {
    outline: none;
    border - color: var(--primary);
    background: white;
    box - shadow: 0 0 0 4px var(--primary - light);
}

    .password - toggle:hover {
    color: var(--primary);
    transform: scale(1.1);
}

    .submit - button:hover {
    background: var(--primary - dark);
    transform: translateY(-1px);
    box - shadow:
    0 4px 12px rgba(59, 130, 246, 0.25),
        0 2px 4px rgba(59, 130, 246, 0.15);
}

    .submit - button: hover.button - glow {
    transform: translateX(100 %);
}

    .login - link:hover {
    color: var(--text - main);
}

    .login - link:hover span {
    color: var(--primary - dark);
}

    .submit - button:active {
    transform: translateY(0);
    box - shadow: none;
}

    .password - toggle:active {
    transform: scale(0.9);
}

    .form - input: not(: placeholder - shown):valid {
    border - color: var(--success);
}

    .form - input: not(: placeholder - shown):valid ~ .input - icon {
    color: var(--success);
}

@keyframes shake {
    0 %, 100 % {
        transform: translateX(0);
    }
    25 % {
        transform: translateX(-4px);
    }
    75 % {
        transform: translateX(4px);
    }
}

    .form - input: not(: placeholder - shown):invalid {
    border - color: #ef4444;
    animation: shake 0.2s ease -in -out;
}

    .form - input: not(: placeholder - shown):invalid ~ .input - icon {
    color: #ef4444;
}
