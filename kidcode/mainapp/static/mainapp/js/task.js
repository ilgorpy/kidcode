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

    const startButton = document.getElementById('startButton'); // Кнопка старт
    let commands = []; // Массив команд
    let commandIndex = 0; // Индекс текущей команды
    let intervalId; // Для хранения идентификатора интервала
    
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


    let isRunning = false; // Флаг, указывающий на состояние выполнения

    startButton.addEventListener('click', () => {
    if (isRunning) {
        // Если код уже выполняется, ничего не делаем
        return;
    }

    const code = editor.getValue().trim();
    const commands = parseCommands(code);
    commandIndex = 0;

    // Устанавливаем флаг выполнения в true
    isRunning = true;

    if (intervalId) {
        clearInterval(intervalId);
    }

    intervalId = setInterval(() => {
        if (commandIndex < commands.length) {
            sendCommand(commands[commandIndex]);
            
            commandIndex++;
        } else {
            clearInterval(intervalId);
            isRunning = false; // Сбрасываем флаг, когда выполнение завершено
        }
    }, 1000);
});
    
    // Функция для разбора команд, включая поддержку циклов
    function parseCommands(code) {
        const lines = code.split('\n');
        const commands = [];
        
        let i = 0;
        while (i < lines.length) {
            const line = lines[i].trim();
            
            // Проверка на наличие цикла
            if (line.startsWith("for _ in range(") && line.endsWith("):")) {
                // Извлекаем число итераций
                const startIndex = line.indexOf('(') + 1;
                const endIndex = line.indexOf(')');
                const iterations = line.slice(startIndex, endIndex);
                const parsedIterations = parseInt(iterations, 10);
                
                if (!isNaN(parsedIterations)) {
                    i++; // Переходим к строкам с командами внутри цикла
                    
                    // Считываем команды внутри цикла
                    const innerCommands = [];
                    while (i < lines.length && lines[i].trim() !== '') {
                        innerCommands.push(lines[i].trim());
                        i++;
                    }
                    
                    // Добавляем команды в массив для каждой итерации
                    for (let j = 0; j < parsedIterations; j++) {
                        commands.push(...innerCommands);
                    }
                    
                    // Если есть пустая строка, пропускаем её
                    i++;
                } else {
                    // Если не удалось распарсить итерации, просто добавляем текущую строку как команду
                    if (line) {
                        commands.push(line);
                    }
                    i++;
                }
            } else {
                // Если это обычная команда, добавляем её в список
                if (line) {
                    commands.push(line);
                }
                i++;
            }
        }
        
        return commands;
    }
    

    function sendCommand(command) {
        // URL для отправки команды
        const url = `/task/${taskId}/${playerId}/`;
        const code = editor.getValue().trim();
        
        
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ code: command, commands: code })
        })
        .then(response => {
            if (!response.ok) { // Проверяем, успешен ли ответ
                return response.json().then(errData => {
                    throw new Error(errData.error || 'Ошибка при сохранении'); // Генерируем ошибку с сообщением
                });
            }
            return response.json(); // Возвращаем JSON-ответ
        })
        .then(data => {
            console.log('Полученные данные:', data); // Логируем полученные данные
            const { x, y } = data;
            updatePlayerPosition(x, y); // Обновляем позицию игрока
            if (data.level_completed) {
                setTimeout(() => alert("Уровень пройден!"), 1000);
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert(error.message);
        });
    }


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
