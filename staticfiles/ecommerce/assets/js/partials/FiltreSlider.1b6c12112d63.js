const container = document.getElementById('filtersContainer');
const btnLeft = document.getElementById('scrollLeft');
const btnRight = document.getElementById('scrollRight');
const scrollStep = 150; // distance à chaque clic

function updateButtons() {
  btnLeft.disabled = container.scrollLeft <= 0;
  btnRight.disabled = container.scrollLeft + container.clientWidth >= container.scrollWidth - 1;
}

btnLeft.addEventListener('click', () => {
  container.scrollBy({ left: -scrollStep, behavior: 'smooth' });
  setTimeout(updateButtons, 400);
});

btnRight.addEventListener('click', () => {
  container.scrollBy({ left: scrollStep, behavior: 'smooth' });
  setTimeout(updateButtons, 400);
});

container.addEventListener('scroll', updateButtons);
window.addEventListener('resize', updateButtons);