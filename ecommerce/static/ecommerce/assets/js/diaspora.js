// Gestion de l'accordéon FAQ
document.addEventListener('DOMContentLoaded', function () {
    const faqItems = document.querySelectorAll('.faq-item');

    faqItems.forEach(item => {
        item.addEventListener('click', () => {
            // Ferme les autres
            faqItems.forEach(otherItem => {
                if (otherItem !== item) {
                    otherItem.classList.remove('active');
                }
            });
            // Bascule l'actuel
            item.classList.toggle('active');
        });
    });
});

// Footer year (copied from Antigaspi1)
const yearSpan = document.getElementById('year-footer');
if (yearSpan) yearSpan.textContent = new Date().getFullYear();

// Theme auto-apply (copied from Antigaspi1)
function applyTheme(){
    var hour = new Date().getHours();
    var isNight = (hour < 7 || hour >= 18);
    var root = document.documentElement;
    root.classList.remove('light-theme','dark-theme');
    root.classList.add(isNight ? 'dark-theme' : 'light-theme');
}

applyTheme();
setInterval(applyTheme, 60 * 1000);
