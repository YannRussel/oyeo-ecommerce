const slides = document.querySelectorAll('.slide-item');
const dots = document.querySelectorAll('.dot-button');
const nextBtn = document.querySelector('.nav-arrow.next-arrow');
const prevBtn = document.querySelector('.nav-arrow.prev-arrow');
let current = 0;

function showSlide(index) {
  slides.forEach(s => s.classList.remove('active-slide'));
  dots.forEach(d => d.classList.remove('active-dot'));
  slides[index].classList.add('active-slide');
  dots[index].classList.add('active-dot');
  current = index;
}

nextBtn.addEventListener('click', () => {
  showSlide((current + 1) % slides.length);
});

prevBtn.addEventListener('click', () => {
  showSlide((current - 1 + slides.length) % slides.length);
});

dots.forEach((dot, i) => {
  dot.addEventListener('click', () => showSlide(i));
});

// Auto défilement (fade toutes les 6s)
setInterval(() => {
  showSlide((current + 1) % slides.length);
}, 6000);
