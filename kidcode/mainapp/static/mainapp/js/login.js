document.addEventListener('DOMContentLoaded', () => {
    const student = document.getElementById('student');
    const teacher = document.getElementById('teacher');
    const input = document.getElementById('id_username');
    const label = document.getElementsByClassName('form-label');

    student.addEventListener('click', () => {
        input.style.display = 'block';
    });

    teacher.addEventListener('click', () => {
        input.style.display = 'none'; 
        input.value = 'rekil49118@gmail.com';
    });
});
