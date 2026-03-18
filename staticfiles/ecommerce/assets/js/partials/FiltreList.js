const btnMoreFiltre = document.getElementById("filtre_detailler");
const blocMoreFiltre = document.getElementById("bloc_filtre_detailler");

btnMoreFiltre.addEventListener('click', () => {
    blocMoreFiltre.classList.toggle("bloc_filtre_detailler_height")
})


function toggleBodyScroll(block) {
    if (block) {
        // Bloquer le scroll
        const scrollY = window.scrollY;
        document.body.dataset.scrollY = scrollY;
        document.body.style.overflow = 'hidden';
        document.body.style.position = 'relative'; // optionnel, parfois utile
        document.body.style.top = `-${scrollY}px`;
    } else {
        // Débloquer le scroll
        const scrollY = parseInt(document.body.dataset.scrollY || '0', 10);
        document.body.style.overflow = '';
        document.body.style.position = '';
        document.body.style.top = '';
        window.scrollTo(0, scrollY);
    }
}