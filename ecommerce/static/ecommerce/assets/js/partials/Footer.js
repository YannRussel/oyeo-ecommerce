



/* **********    TYPE WRIPPER **************** */
function startTypewriter(elementId, items, speed = 100, eraseSpeed = 50, delayBetween = 1000) {
    let index = 0;
    let charIndex = 0;
    let isDeleting = false;

    const output = document.getElementById(elementId);

    function type() {
        const current = items[index];

        // Applique la couleur si définie
        if (current.color) {
            output.style.color = current.color;
            output.style.fontWeight = 'bolder';
            output.style.textTransform = 'Capitalize';
        }

        if (!isDeleting) {
            // Écriture
            output.innerHTML = current.icon + " " + current.text.slice(0, charIndex + 1); charIndex++;

            if (charIndex === current.text.length) {
                // Attendre avant d'effacer
                isDeleting = true;
                setTimeout(type, delayBetween);
                return;
            }
        } else {
            // Effacement
            output.textContent = current.text.slice(0, charIndex - 1);
            charIndex--;

            if (charIndex === 0) {
                // Texte suivant
                isDeleting = false;
                index = (index + 1) % items.length;
            }
        }

        setTimeout(type, isDeleting ? eraseSpeed : speed);
    }

    type();
}




const messagesMarketing = [
    {
        text: "Profitez de nos offres exclusives !",
        color: "#e63946",
        icon: "<i class='fas fa-tags'></i>"
    },
    {
        text: "Découvrez nos nouvelles tendances.",
        color: "#1d3557",
        icon: "<i class='fas fa-fire'></i>"
    },
    {
        text: "Nos milliers de clients satisfaits !",
        color: "#f4a261",
        icon: "<i class='fas fa-smile'></i>"
    }
];


// Lancer l'effet
startTypewriter("livraison-bloc", messagesMarketing);
//initMobileAccordion("navbarre_linkCategorie", "sub-menu-1");