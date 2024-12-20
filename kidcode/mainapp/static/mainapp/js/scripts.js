document.addEventListener("DOMContentLoaded", function() {
    loadChapters();  // Загружаем главы при загрузке страницы
});

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('active'); // Переключаем видимость боковой панели
}

function loadChapters() {
    fetch('/chapters/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const chapterList = document.getElementById('chapter-list');
            chapterList.innerHTML = ''; // Очищаем список перед добавлением новых элементов
            data.forEach(chapter => {
                const li = document.createElement('li');
                const a = document.createElement('a');
                a.textContent = chapter;
                a.href = '#';
                a.onclick = () => loadLevels(chapter);

                li.appendChild(a);
                const ul = document.createElement('ul');
                ul.className = 'dropdown';
                ul.id = chapter;
                ul.style.display = 'none';

                li.appendChild(ul);


                chapterList.appendChild(li);
            });
        })
        .catch(error => {
            console.error('Ошибка при загрузке глав:', error);
        });
}

function loadLevels(chapterName) {
    const dropdown = document.getElementById(chapterName);
    dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';

    // Если уровни еще не загружены, загружаем их
    if (dropdown.children.length === 0) {
        fetch(`/levels/${chapterName}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // data - это объект, где ключи - это id задач, а значения - названия уровней
                Object.entries(data).forEach(([task_id, levelName]) => {
                    const li = document.createElement('li');
                    const link = document.createElement('a');

                    // Устанавливаем href для перенаправления на страницу задачи
                    link.href = `/task/${task_id}`; // Используем taskId как идентификатор задачи
                    link.textContent = levelName; // Устанавливаем текст ссылки как название уровня

                    li.appendChild(link); // Добавляем ссылку в элемент li
                    dropdown.appendChild(li);
                });
            })
            .catch(error => {
                console.error('Ошибка при загрузке уровней:', error);
            });
    }
}