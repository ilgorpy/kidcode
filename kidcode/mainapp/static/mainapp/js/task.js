document.addEventListener('DOMContentLoaded', () => {
    // Настройка элементов
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    
    // Получаем идентификатор задачи из URL (или передайте его другим способом)
    const taskId = window.location.pathname.split('/')[2]; // Например, из '/task/1/' извлекаем '1'

    // URL для загрузки данных игрового поля
    const gameDataUrl = `/task/${taskId}/data/`;

    // Загружаем JSON-данные игрового поля
    fetch(gameDataUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Ошибка HTTP: ${response.status}`);
            }
            return response.json();
        })
        .then(gameField => {
            // Данные игрового поля
            const data = gameField.data;
            const width = gameField.width;
            const height = gameField.height;

            // Устанавливаем размеры canvas
            canvas.width = width * 64; // 64px — размер клетки
            canvas.height = height * 64;

            // Подготовка изображений
            const images = {
                cube: new Image(),
                hole: new Image(),
                block: new Image()
            };
            images.cube.src = "/static/mainapp/images/cube.png";   // Путь к изображениям
            images.hole.src = "/static/mainapp/images/hole.png";
            images.block.src = "/static/mainapp/images/block.png";

            // Отрисовка игрового поля
            Promise.all([
                loadImage(images.cube),
                loadImage(images.hole),
                loadImage(images.block)
            ]).then(() => {
                drawGrid(width, height);
                data.forEach(item => {
                    const { x, y, id } = item;
                    ctx.drawImage(images[id], x, y, 64, 64); // Рисуем объект на поле
                });
            });
        })
        .catch(error => {
            console.error('Ошибка загрузки данных игрового поля:', error);
        });

    // Утилита для загрузки изображений
    function loadImage(img) {
        return new Promise((resolve, reject) => {
            img.onload = () => resolve(img);
            img.onerror = reject;
        });
    }

    function drawGrid(width, height) {
        ctx.strokeStyle = '#cccccc'; // Цвет линий сетки
        ctx.lineWidth = 1; // Толщина линий

        for (let x = 0; x <= width; x++) {
            ctx.beginPath();
            ctx.moveTo(x * 64, 0); // Начало линии по вертикали
            ctx.lineTo(x * 64, height * 64); // Конец линии по вертикали
            ctx.stroke();
        }

        for (let y = 0; y <= height; y++) {
            ctx.beginPath();
            ctx.moveTo(0, y * 64); // Начало линии по горизонтали
            ctx.lineTo(width * 64, y * 64); // Конец линии по горизонтали
            ctx.stroke();
        }
    }
});
