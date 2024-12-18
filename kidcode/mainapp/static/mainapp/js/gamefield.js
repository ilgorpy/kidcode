document.addEventListener('DOMContentLoaded', () => {
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

    const placedObjects = []; // Массив для хранения размещённых объектов
    const difficultySelect = document.querySelectorAll('#id_difficult');
    const form_auto = document.getElementById('autoForm');

    difficultySelect.forEach(select => {
        select.addEventListener('change', () => {
            const selectedDifficulty = select.value;
            if (selectedDifficulty === 'easy') {
                jsonData = {
                    'width': 4,
                    'height': 4,
                    'cube': 2,
                    'hole': 3,
                    'block': 2,
                    'data': [{"x": 120, "y": 120}]
                }
            }
            if (selectedDifficulty === 'medium') {
                jsonData = {
                    'width': 5,
                    'height': 5,
                    'cube': 3,
                    'hole': 4,
                    'block': 3,
                    'data': [{"x": 120, "y": 120}]
                }
            }
            
            if (selectedDifficulty === 'hard') {
                jsonData = {
                    'width': 8,
                    'height': 8,
                    'cube': 10,
                    'hole': 6,
                    'block': 3,
                    'data': [{"x": 120, "y": 120}]
                }
            }
            gridWidth = jsonData['width'];
            gridHeight = jsonData['height'];
            console.log(selectedDifficulty);
            fetch('/constructor/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify(jsonData)
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                alert('Сохранение прошло успешно!');
            })
            .catch(error => {
                console.error('Ошибка:', error);
                alert('Произошла ошибка при сохранении.');
            });
            drawGrid();
        }); 
    });

    

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
        const newGridWidth = parseInt(gridWidth.value, 10);
        const newGridHeight = parseInt(gridHeight.value, 10);

        if (isNaN(newGridWidth) || isNaN(newGridHeight)) {
            return;
        }

        if (newGridHeight > 10 || newGridWidth > 10 || newGridHeight < 4 || newGridWidth < 4) {
            alert('Допустимый диапазон значений от 4 до 10. Попробуйте снова');
            return;
        }

        if (newGridHeight !== newGridWidth) {
            alert('Поле должно быть квадратным');
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
                id: template.id
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
            // Добавляем объект обратно в массив
            placedObjects.push({
                image: currentTemplate.image,
                x: currentTemplate.x,
                y: currentTemplate.y,
                id: currentTemplate.id
            });

            currentTemplate = null;
            isDragging = false;

            drawGrid();
        }
    });

    gridWidth.addEventListener('blur', updateCanvasSize);
    gridHeight.addEventListener('blur', updateCanvasSize);

    drawGrid();

    


    const saveButton = document.getElementById('saveButton');
    const form = document.getElementById('manualForm');

    form.addEventListener('submit', function (e) {
        e.preventDefault(); // Отключаем стандартное поведение формы
        // Собираем данные из формы
        const formData = new FormData(form);
        const jsonData = {};
        formData.forEach((value, key) => {
            jsonData[key] = value;
        });

        // Добавляем дополнительные данные (например, координаты из canvas)
        jsonData.iconPosition = placedObjects; // Это пример, замените на реальные координаты

        // Отправляем данные через fetch
        fetch('/constructor/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': formData.get('csrfmiddlewaretoken') // Передаём CSRF токен
            },
            body: JSON.stringify(jsonData)
        })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                alert('Сохранение прошло успешно!');
            })
            .catch(error => {
                console.error('Ошибка:', error);
                alert('Произошла ошибка при сохранении.');
            });
    });
});

