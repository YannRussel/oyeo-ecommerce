
        document.addEventListener("DOMContentLoaded", function () {
            if (window.innerWidth < 982) {

                function initAccordion(btnClass, panelClass, level) {
                    let buttons = document.getElementsByClassName(btnClass);

                    for (let btn of buttons) {
                        btn.addEventListener("click", function () {
                            let panel = this.nextElementSibling;

                            if (!panel || !panel.classList.contains(panelClass)) return;

                            // ---------- NIVEAU 1 ----------
                            if (level === 1) {

                                // Si ce bouton est déjà actif → fermer et sortir
                                if (this.classList.contains("active")) {
                                    this.classList.remove("active");
                                    panel.style.display = "none";

                                    // Fermer aussi tout le niveau 2 dans ce panel
                                    panel.querySelectorAll(".panel_n2").forEach(p2 => p2.style.display = "none");
                                    panel.querySelectorAll(".accordion_n2").forEach(b2 => b2.classList.remove("active"));

                                    return;
                                }

                                // Fermer tous les panels niveau 1
                                document.querySelectorAll("." + panelClass).forEach(p => p.style.display = "none");
                                document.querySelectorAll("." + btnClass).forEach(b => b.classList.remove("active"));

                                // Fermer tous les panels niveau 2
                                document.querySelectorAll(".panel_n2").forEach(p2 => p2.style.display = "none");
                                document.querySelectorAll(".accordion_n2").forEach(b2 => b2.classList.remove("active"));

                                // Ouvrir celui demandé
                                this.classList.add("active");
                                panel.style.display = "block";

                                return;
                            }


                            // ---------- NIVEAU 2 ----------
                            if (level === 2) {

                                // Toggle : si déjà ouvert → fermer
                                if (this.classList.contains("active")) {
                                    this.classList.remove("active");
                                    panel.style.display = "none";
                                    return;
                                }

                                // Trouver le panel parent de niveau 1
                                let parentPanel = this.closest(".panel");

                                // Fermer seulement les niveaux 2 dans ce panel parent
                                parentPanel.querySelectorAll(".panel_n2").forEach(p2 => p2.style.display = "none");
                                parentPanel.querySelectorAll(".accordion_n2").forEach(b2 => b2.classList.remove("active"));

                                // Ouvrir celui demandé
                                this.classList.add("active");
                                panel.style.display = "block";
                            }
                        });
                    }
                }


                /* function applyAccordionAnimations() {
                    const observer = new MutationObserver((mutations) => {
                        for (let m of mutations) {
                            if (m.attributeName === "style") {
                                let panel = m.target;
                
                                if (panel.style.display === "block") {
                                    panel.classList.add("open");
                                } else {
                                    panel.classList.remove("open");
                                }
                            }
                        }
                    });
                
                   
                    document.querySelectorAll(".panel, .panel_n2").forEach(panel => {
                        observer.observe(panel, { attributes: true });
                    });
                } */

                /* applyAccordionAnimations(); */



                // ---- Initialisation ----
                initAccordion("accordion", "panel", 1);          // Niveau 1
                initAccordion("accordion_n2", "panel_n2", 2);    // Niveau 2












            }
        });


