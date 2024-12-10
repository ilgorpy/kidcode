document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    const cellSize = 60; 
    let gridWidth = document.getElementById('id_width');
    let gridHeight = document.getElementById('id_height');

    canvas.width = gridWidth * cellSize;
    canvas.width = gridWidth * cellSize;


    if (!canvas || !gridWidth || !gridHeight ) {
        console.error("Один или несколько элементов не найдены!");
        return;
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
    }

    function updateCanvasSize() {
        const newGridWidth = parseInt(gridWidth.value, 10);
        const newGridHeight = parseInt(gridHeight.value, 10);

        if (isNaN(newGridWidth) || isNaN(newGridHeight)) {
            return; 
        }


        if(newGridHeight > 10 || newGridWidth > 10 || newGridHeight < 4 || newGridWidth < 4)
        {
            alert('Допустимый диапозон значений от 4 до 10. Попробуйте снова')
            return;
        }

        
        if (newGridHeight != newGridWidth) {
            alert('Поле должно быть квадратным');
            return;
        }

        canvas.width = newGridWidth * cellSize;
        canvas.height = newGridHeight * cellSize;

        drawGrid(); 
    }

    
    gridWidth.addEventListener('blur', updateCanvasSize);
    gridHeight.addEventListener('blur', updateCanvasSize);

   
    drawGrid();
});

