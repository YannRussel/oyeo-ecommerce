document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("demoContainer");
    const btnLeft = document.getElementById("demoLeft");
    const btnRight = document.getElementById("demoRight");

    // Distance de défilement (ajuste si besoin)
    const scrollAmount = 300;

    // Scroll vers la droite
    btnRight.addEventListener("click", () => {
        container.scrollBy({
            left: scrollAmount,
            behavior: "auto"
        });
    });

    // Scroll vers la gauche
    btnLeft.addEventListener("click", () => {
        container.scrollBy({
            left: -scrollAmount,
            behavior: "auto"
        });
    });

    // Activer / désactiver les boutons selon la position
    const updateButtons = () => {
        btnLeft.disabled = container.scrollLeft <= 0;
        btnRight.disabled =
            container.scrollLeft + container.clientWidth >= container.scrollWidth - 1;
    };

    // Écoute le scroll
    container.addEventListener("scroll", updateButtons);

    // Initialisation
    updateButtons();
});