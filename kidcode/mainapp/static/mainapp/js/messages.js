function showPopup(message) {
    const popup = document.getElementById('popup-message');
    const text = document.getElementById('popup-text');

    text.textContent = message;  // Устанавливаем текст сообщения
    popup.classList.remove('hidden');  // Показываем окно

    setTimeout(() => {
        popup.classList.add('hidden');  // Скрываем окно через 3 секунды();
    }, 3500);
}

function closePopup() {
    const popup = document.getElementById('popup-message');
    popup.classList.add('hidden');  // Скрываем окно
}