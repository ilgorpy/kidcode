document.addEventListener('DOMContentLoaded', () => {
    let playerStart = { x: 0, y: 0 };
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    const cellSize = 64; 
    let gridWidth = document.getElementById('id_width');
    let gridHeight = document.getElementById('id_height');
    canvas.width = gridWidth * cellSize;
    canvas.height = gridHeight * cellSize;
    //Drag and drop
    const templates = document.querySelectorAll('.template');
    let isDragging = false; // Флаг для отслеживания процесса перетаскивания
    let currentTemplate = null; // Текущий шаблон, который перетаскивается
    let offsetX = 0; // Смещение для корректного размещения
    let offsetY = 0;

    let placedObjects = []; // Массив для хранения размещённых объектов
   
    const manualform = document.getElementById('manualForm');
    const autoform = document.getElementById('autoForm');
    const textform = document.getElementById('textForm');
    const generateButton = document.getElementById('generateButton');
    const difficultySelect = document.getElementById('id_difficult');
    const autoButton = document.getElementById('autoButton');
    const savemanual = document.getElementById('savemanual');
    const saveauto = document.getElementById('saveauto');
    let randomData = {};

    const cubeInput = document.getElementById('id_cube'); // Поле "Количество кубиков"
    const holeInput = document.getElementById('id_hole'); // Поле "Количество лунок"
    const blockInput = document.getElementById('id_block'); // Поле "Количество занятых клеток"

  
    // Переменные для отслеживания лимитов
    let maxCubes = parseInt(cubeInput.value, 10) || 0;
    let maxHoles = parseInt(holeInput.value, 10) || 0;
    let maxBlocks = parseInt(blockInput.value, 10) || 0;

 
        const manualButton = document.getElementById('manualButton');
        const manualForm = document.getElementById('manualForm');
    
        autoButton.addEventListener('click', () => {
            clearField(); // Очищаем поле
            manualForm.style.display = 'none'; // Скрываем ручную форму
            generateButton.style.display = 'block';
            saveauto.style.display = 'block';
            savemanual.style.display = 'none';
        });
    
        manualButton.addEventListener('click', () => {
            clearField(); // Очищаем поле
            manualForm.style.display = 'block'; // Показываем ручную форму
            generateButton.style.display = 'none';
            saveauto.style.display = 'none';
            savemanual.style.display = 'block';
        });
       
        

    // Слушатели для обновления лимитов при изменении полей ввода
    cubeInput.addEventListener('input', () => {
        maxCubes = parseInt(cubeInput.value, 10) || 0;
    });
    holeInput.addEventListener('input', () => {
        maxHoles = parseInt(holeInput.value, 10) || 0;
    });
    blockInput.addEventListener('input', () => {
        maxBlocks = parseInt(blockInput.value, 10) || 0;
    });

    function clearField() {
        placedObjects = []; // Очищаем массив объектов
        gridWidth.value = 4; // Минимальное значение ширины
        gridHeight.value = 4; // Минимальное значение высоты
        canvas.width = 4 * cellSize; // Устанавливаем минимальный размер canvas
        canvas.height = 4 * cellSize;
        drawGrid(); // Перерисовываем сетку
    }

    generateButton.addEventListener("click", function () {
        const selectedDifficulty = difficultySelect.value; // Получаем выбранный уровень
        if (selectedDifficulty === 'easy') {
            randomData = {
                'width': 4,
                'height': 4,
                'cube': 2,
                'hole': 3,
                'block': 1,
            };
        } else if (selectedDifficulty === 'medium') {
            randomData = {
                'width': 6,
                'height': 6,
                'cube': 3,
                'hole': 4,
                'block': 2,
            };
        } else if (selectedDifficulty === 'hard') {
            randomData = {
                'width': 8,
                'height': 8,
                'cube': 5,
                'hole': 6,
                'block': 3,
            };
        }
    
        gridWidth = randomData['width'];
        gridHeight = randomData['height'];
        canvas.width = gridWidth * cellSize;
        canvas.height = gridHeight * cellSize;
    
        placedObjects = generateObjects(randomData); // Генерируем объекты
        drawGrid(); // Перерисовываем сетку
    });

    function generateObjects(randomData) {
        const generatedObjects = []; // Массив для хранения объектов
    
        const addObject = (type, count) => {
            let placed = 0;
            while (placed < count) {
                const x = Math.floor(Math.random() * gridWidth) * cellSize;
                const y = Math.floor(Math.random() * gridHeight) * cellSize;
                // Проверяем, занята ли клетка
                const isOccupied = generatedObjects.some(obj => obj.x === x && obj.y === y);
                if (!isOccupied) {
                    generatedObjects.push({
                        image: (() => {
                            const img = new Image();
                            if (type === 'cube') img.src = cubeImage;
                            else if (type === 'hole') img.src = holeImage;
                            else if (type === 'block') img.src = blockImage;
                            else if (type == 'player') img.src = playerImage;
                            else if (type == 'goal') img.src = goalImage;
                            return img;
                        })(),
                        x: x,
                        y: y,
                        id: type
                    });
                    placed++;
                }
            }
        };
    
        // Добавляем объекты по типу
        addObject('goal', 1)
        addObject('cube', randomData.cube); // Кубики
        addObject('hole', randomData.hole); // Лунки
        addObject('block', randomData.block); // Блоки
        addObject('player', 1);
    
        return generatedObjects;
    }


    function drawGrid() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        ctx.strokeStyle = "#FFFFFF";

        for (let x = 0; x <= canvas.width; x += cellSize) {
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, canvas.height);
            ctx.stroke();
        }

        for (let y = 0; y <= canvas.height; y += cellSize) {
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(canvas.width, y);
            ctx.stroke();
        }

        placedObjects.forEach(obj => {
            ctx.drawImage(obj.image, obj.x, obj.y, cellSize, cellSize);
        });
    }

    function updateCanvasSize() {
        const newGridWidth = parseInt(document.getElementById('id_width').value, 10); // Считываем значение ширины
        const newGridHeight = parseInt(document.getElementById('id_height').value, 10); // Считываем значение высоты

        if (isNaN(newGridWidth) || isNaN(newGridHeight)) {
    
            return;
        }

        if (newGridHeight > 10 || newGridWidth > 10 || newGridHeight < 4 || newGridWidth < 4) {
            alert('Допустимый диапазон значений от 4 до 10. Попробуйте снова');
            return;
        }

        
        canvas.width = newGridWidth * cellSize;
        canvas.height = newGridHeight * cellSize;

        drawGrid();
    }

    function getObjectAtPosition(x, y) {
        return placedObjects.find(obj =>
            x >= obj.x &&
            x < obj.x + cellSize &&
            y >= obj.y &&
            y < obj.y + cellSize
        );
    }

    // Перетаскивание шаблона из списка
    templates.forEach(template => {
        template.addEventListener('mousedown', e => {
            const rect = template.getBoundingClientRect();

            currentTemplate = {
                image: new Image(),
                x: 0,
                y: 0,
                id: template.dataset.type // Получаем тип объекта из data-type
            };
            currentTemplate.image.src = template.src;
            offsetX = e.clientX - rect.left;
            offsetY = e.clientY - rect.top;

            isDragging = true;
        });
    });

    // Начало перетаскивания на canvas
    canvas.addEventListener('mousedown', e => {
        const rect = canvas.getBoundingClientRect();
        const mouseX = e.clientX - rect.left;
        const mouseY = e.clientY - rect.top;

        const selectedObject = getObjectAtPosition(mouseX, mouseY);
        if (selectedObject) {
            currentTemplate = selectedObject;
            isDragging = true;

            offsetX = mouseX - selectedObject.x;
            offsetY = mouseY - selectedObject.y;

            // Удаляем объект из массива, чтобы избежать дублирования
            const index = placedObjects.indexOf(selectedObject);
            if (index > -1) placedObjects.splice(index, 1);
        }
    });

    // Перемещение объекта
    canvas.addEventListener('mousemove', e => {
        if (isDragging && currentTemplate) {
            const rect = canvas.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            const mouseY = e.clientY - rect.top;

            currentTemplate.x = Math.floor((mouseX - offsetX) / cellSize) * cellSize;
            currentTemplate.y = Math.floor((mouseY - offsetY) / cellSize) * cellSize;

            drawGrid();
            ctx.drawImage(
                currentTemplate.image,
                currentTemplate.x,
                currentTemplate.y,
                cellSize,
                cellSize
            );
        }
    });

    // Завершение перетаскивания
    canvas.addEventListener('mouseup', () => {
        if (isDragging && currentTemplate) {
            // Подсчитываем количество объектов текущего типа
            const objectCount = placedObjects.filter(obj => obj.id === currentTemplate.id).length;
    
            let limitExceeded = false;
    
            if (currentTemplate.id === 'cube' && objectCount >= maxCubes) {
                alert('Превышено количество кубиков!');
                limitExceeded = true;
            } else if (currentTemplate.id === 'hole' && objectCount >= maxHoles) {
                alert('Превышено количество лунок!');
                limitExceeded = true;
            } else if (currentTemplate.id === 'block' && objectCount >= maxBlocks) {
                alert('Превышено количество блоков!');
                limitExceeded = true;
            }
            else if (currentTemplate.id === 'player' && objectCount >= 1) {
                alert('Превышено количество игроков!');
                limitExceeded = true;
            }
            else if (currentTemplate.id === 'goal' && objectCount >= 1) {
                alert('Превышено количество целей!');
                limitExceeded = true;
            }
                
            
    
            if (!limitExceeded) {
                // Проверяем, занята ли клетка
                const isOccupied = placedObjects.some(obj =>
                    obj.x === currentTemplate.x && obj.y === currentTemplate.y
                );
    
                if (!isOccupied) {
                    // Добавляем объект в массив, если клетка не занята и лимит не превышен
                    placedObjects.push({
                        image: currentTemplate.image,
                        x: currentTemplate.x,
                        y: currentTemplate.y,
                        id: currentTemplate.id
                    });
                } else {
                    alert('Эта клетка уже занята!');
                }
            }
    
            currentTemplate = null;
            isDragging = false;
    
            drawGrid(); // Перерисовываем сетку
        }
    });

    // Событие для удаления объекта
canvas.addEventListener('dblclick', (e) => {
    const rect = canvas.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;

    const objectToRemove = getObjectAtPosition(mouseX, mouseY);
    if (objectToRemove) {
        // Удаляем объект из массива
        const index = placedObjects.indexOf(objectToRemove);
        if (index > -1) {
            placedObjects.splice(index, 1);
        }
        drawGrid(); // Перерисовываем сетку
    }
});

    gridWidth.addEventListener('blur', updateCanvasSize);
    gridHeight.addEventListener('blur', updateCanvasSize);

    drawGrid();


    //Функция для обработки ручного поля
    savemanual.addEventListener('click', function (e) {
        e.preventDefault(); // Отключаем стандартное поведение формы
        if (placedObjects.length === 0) {
            alert('Поле пустое! Пожалуйста, добавьте объекты перед сохранением.');
            return; // Останавливаем выполнение функции
        }
        // Собираем данные из формы
        const formData = new FormData(textform);
        const formData2 = new FormData(manualform);
        const jsonData = {};
        formData.forEach((value, key) => {
            jsonData[key] = value;
        });
        formData2.forEach((value, key) => {
            jsonData[key] = value;
        });
        // Добавляем дополнительные данные (например, координаты из canvas)
        jsonData.data = placedObjects; 
        console.log(jsonData);
        // Отправляем данные через fetch
        fetch('/constructor/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': formData.get('csrfmiddlewaretoken') // Передаём CSRF токен
            },
            body: JSON.stringify(jsonData)
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
            console.log(data);
            alert('Сохранение прошло успешно!');
        })
            .catch(error => {
                console.error('Ошибка:', error);
                alert(error.message);
            });
    });

    //Функция для обработки автоматического поля
    saveauto.addEventListener('click', function (e) {
        e.preventDefault(); // Отключаем стандартное поведение формы
        if (placedObjects.length === 0) {
            alert('Поле пустое! Пожалуйста, добавьте объекты перед сохранением.');
            return; // Останавливаем выполнение функции
        }
        // Собираем данные из формы
        const formData = new FormData(textform);
        const jsonData = {};
        formData.forEach((value, key) => {
            jsonData[key] = value;
        });
        Object.assign(jsonData, randomData);
        jsonData.data = placedObjects; 
        jsonData.playerStart = playerStart;
        // Отправляем данные через fetch
        fetch('/constructor/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': formData.get('csrfmiddlewaretoken') // Передаём CSRF токен
            },
            body: JSON.stringify(jsonData)
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
            console.log(data);
            alert('Сохранение прошло успешно!');
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert('Произошла ошибка при сохранении: ' + error.message); // Выводим сообщение об ошибке
        });
    });

});

