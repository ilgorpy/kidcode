document.addEventListener('DOMContentLoaded', () => {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let data = [];
    //Поля для canvas
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    
    // Получаем идентификатор задачи из URL (или передайте его другим способом)
    const taskId = window.location.pathname.split('/')[2]; // Например, из '/task/1/' извлекаем '1'

    // URL для загрузки данных игрового поля
    const gameDataUrl = `/task/${taskId}/data/`;
    
    //Элементы для подсказки
    const clueButton = document.getElementById('clueButton');
    const clueModal = document.getElementById('clueModal');
    const closeClue = document.getElementById('closeClue');
    const clueText = document.getElementById('clueText');
    
    const images = {
        cube: new Image(),
        hole: new Image(),
        block: new Image(),
        player: new Image(),
        goal: new Image()
    };

    // Элементы для учебника
    const manualButton = document.getElementById('guideButton');
    const manualModal = document.getElementById('manualModal');
    const closeManual = document.getElementById('closeManual');

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
        data = gameField.data;
        const width = gameField.width;
        const height = gameField.height;

        // Устанавливаем размеры canvas
        canvas.width = width * 64; // 64px — размер клетки
        canvas.height = height * 64;

        // Подготовка изображений
        images.cube.src = "/static/mainapp/images/cube.png";   // Путь к изображениям
        images.hole.src = "/static/mainapp/images/hole.png";
        images.block.src = "/static/mainapp/images/block.png";
        images.player.src = "/static/mainapp/images/pixel-last.png";
        images.goal.src = "/static/mainapp/images/goal.png";

        // Отрисовка игрового поля
        Promise.all([
            loadImage(images.cube),
            loadImage(images.hole),
            loadImage(images.block),
            loadImage(images.player),
            loadImage(images.goal)
        ]).then(() => {
            drawGrid(width, height);
            data = data.filter(item => item.id !== 'player');
            data.forEach(item => {
                const { x, y, id } = item;
                ctx.drawImage(images[id], x, y, 64, 64); // Рисуем объект на поле
            });

            // Отрисовка игрока на поле
            ctx.drawImage(images.player, playerX , playerY , 64, 64);  // playerX и playerY передаются из шаблона
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
       // Открытие и закрытие модального окна для подсказки
       clueButton.addEventListener('click', async () => {
        try {
            const response = await fetch(`/task/${taskId}/clue/`);
            if (!response.ok) throw new Error(`Ошибка HTTP: ${response.status}`);
            const data = await response.json();
            clueText.textContent = data.clue; // Отображение подсказки
        } catch (error) {
            clueText.textContent = 'Ошибка загрузки подсказки.';
            console.error('Ошибка загрузки подсказки:', error);
        }
        clueModal.style.display = 'block';
    });

    closeClue.addEventListener('click', () => {
        clueModal.style.display = 'none';
    });

    // Открытие и закрытие модального окна для учебника
    manualButton.addEventListener('click', () => {
        manualModal.style.display = 'block';
    });

    closeManual.addEventListener('click', () => {
        manualModal.style.display = 'none';
    });

    // Закрытие модальных окон при клике вне их
    window.addEventListener('click', (event) => {
        if (event.target === clueModal) {
            clueModal.style.display = 'none';
        }
        if (event.target === manualModal) {
            manualModal.style.display = 'none';
        }
    });

    document.getElementById('startButton').addEventListener('click', async () => {
        const code = editor.getValue().trim();
        console.log('Code:', code);
        try {
            const response = await fetch(`/task/${taskId}/${playerId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify({ code }),
            });
    
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `Ошибка HTTP: ${response.status}`);
            }
    
            const dataResponse = await response.json();
            console.log(dataResponse);
    
            if (dataResponse.level_completed) {
                Swal.fire({
                    title: 'Поздравляем!',
                    text: dataResponse.message || 'Уровень пройден!',
                    background: '#22231E',
                    color: '#ffffff',
                    confirmButtonColor: '#0EA524',
                    icon: 'success',
                    confirmButtonText: 'OK',
                });
            } else if (dataResponse.error) {
                Swal.fire({
                    title: 'Ошибка!',
                    text: dataResponse.error,
                    background: '#22231E',
                    color: '#ffffff',
                    confirmButtonColor: '#FF0000',
                    icon: 'error',
                    confirmButtonText: 'OK',
                });
            } else {
                const { x, y } = dataResponse;
    
                // Обновляем координаты игрока
                const playerData = data.find(item => item.id === 'player');
                if (playerData) {
                    playerData.x = x;
                    playerData.y = y;
                }
    
                // Обновляем игровое поле
                updatePlayerPosition(x, y);
            }
        } catch (error) {
            console.error('Ошибка выполнения кода:', error);
            Swal.fire({
                title: 'Ошибка выполнения!',
                text: error.message || 'Неизвестная ошибка',
                background: '#22231E',
                color: '#ffffff',
                confirmButtonColor: '#FF0000',
                icon: 'error',
                confirmButtonText: 'OK',
            });
        }
    });
    
    
    

    

    function updatePlayerPosition(x, y) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    
        // Перерисуем сетку
        drawGrid(canvas.width / 64, canvas.height / 64);
    
        // Перерисовываем все элементы
        data.forEach(item => {
            const { x, y, id } = item;
            ctx.drawImage(images[id], x, y, 64, 64); // Рисуем объект на поле
        });
    
        // Обновляем глобальные переменные и рисуем игрока
        playerX = x; // перевод в пиксели
        playerY = y;
        console.log(playerX, playerY);
        ctx.drawImage(images.player, playerX, playerY, 64, 64);
    }
    
    document.getElementById('clearButton').addEventListener('click', function() {


        // Формируем URL для POST-запроса
        const url = `/task/${taskId}/reset/${playerId}/`;

        // Отправляем POST-запрос на сервер
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({})  // Мы не передаем никаких данных в теле запроса
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Данные очищены успешно!');
                // Обновляем страницу или выполняем другие действия
                location.reload();  // Перезагружаем страницу, чтобы обновить игровое поле и данные
            } else {
                alert('Ошибка при очистке данных: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert('Произошла ошибка при очистке данных.');
        });
    });

    document.getElementById('sendButton').addEventListener('click', function() {
        
   
    
        // Выполняем fetch-запрос
        fetch(`/task/${taskId}/submit_grade/${playerId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,  // Добавляем CSRF-токен для защиты от CSRF-атак
            },
            body: JSON.stringify({}),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Задание отправлено на проверку!');
            } else {
                alert('Ошибка: ' + data.error);
            }
        })
        .catch(error => {
            alert('Произошла ошибка: ' + error.message);
        });
    });

});
