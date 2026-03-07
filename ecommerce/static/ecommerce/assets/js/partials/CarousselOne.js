document.addEventListener('DOMContentLoaded', function() {
    const slides = document.querySelectorAll('.slide-item');
    const dots = document.querySelectorAll('.dot-button');
    const nextBtn = document.querySelector('.nav-arrow.next-arrow');
    const prevBtn = document.querySelector('.nav-arrow.prev-arrow');
    let current = 0;

    function showSlide(index) {
      if (slides.length === 0) return;
      
      slides.forEach(s => s.classList.remove('active-slide'));
      
      if (slides[index]) {
          slides[index].classList.add('active-slide');
      }

      // Gérer les points uniquement s'ils existent
      if (dots.length > 0) {
          dots.forEach(d => d.classList.remove('active-dot'));
          if (dots[index]) {
              dots[index].classList.add('active-dot');
          }
      }
      
      current = index;
    }

    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
          showSlide((current + 1) % slides.length);
        });
    }

    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
          showSlide((current - 1 + slides.length) % slides.length);
        });
    }

    if (dots.length > 0) {
        dots.forEach((dot, i) => {
          dot.addEventListener('click', () => showSlide(i));
        });
    }

    // Auto défilement (fade toutes les 6s) si on a plus d'une slide
    if (slides.length > 1) {
        setInterval(() => {
          showSlide((current + 1) % slides.length);
        }, 6000);
    }
});
