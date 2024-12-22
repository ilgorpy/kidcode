document.addEventListener("DOMContentLoaded", function () {
    const links = document.querySelectorAll('.profile_btn'); // Все ссылки в меню
    const currentUrl = window.location.pathname; // Текущий URL-адрес
    
    links.forEach(link => {
      // Сравниваем href ссылки с текущим URL
      if (link.getAttribute('href') === currentUrl) {
        link.classList.add('active'); // Добавляем класс активной ссылке
      }
    });
  });