const gradeSelects = document.querySelectorAll('.grade-select');
const saveButton = document.querySelector('.save-btn');

gradeSelects.forEach(select => {
    select.addEventListener('change', async () => {
      const row = select.closest('tr');
      const gradeId = row.dataset.gradeId; // Исправлено имя переменной
      const newGrade = select.value;

      console.log("gradeId:", gradeId); // Добавьте это для отладки
      console.log("newGrade:", newGrade); // Добавьте это для отладки
  
      try {
        const response = await fetch('/update_grade/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
          },
          body: `grade_id=${gradeId}&new_grade=${newGrade}` // Исправлено использование template literals
        });
  
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || 'Ошибка обновления оценки');
        }
  
        console.log('Оценка обновлена успешно!');
      } catch (error) {
        console.error('Ошибка:', error);
      }
    });
  });
  
