document.addEventListener('DOMContentLoaded', () => {
    const student = document.getElementById('student');
    const teacher = document.getElementById('teacher');
    const input = document.getElementById('id_username');
    const label = document.querySelector('label[for="id_username"]');

    student.addEventListener('click', () => {
        input.style.display = 'block';
        if (label) {
            label.style.display = 'block'; // Показываем соответствующий label
        }
    });

    teacher.addEventListener('click', () => {
        input.style.display = 'none'; 
        input.value = 'rekil49118@gmail.com';
        if (label) {
            label.style.display = 'none'; // Скрываем соответствующий label
        }
    });
});
