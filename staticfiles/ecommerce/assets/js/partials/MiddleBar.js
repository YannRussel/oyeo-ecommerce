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

        const btnMenu = document.getElementById('menubtn');
        const btnMenuClose = document.getElementById('menubtnFermer');

        const blocnaviguation = document.getElementById("allnavigationBar");
        const body = document.body;

        btnMenu.addEventListener('click', () => {
            blocnaviguation.classList.add("activeDesactive");

            // toggleScroll();body.classList.toggle("body-limited");
            /*  if (body.classList.contains("no-scroll")) { */
            // remonte tout en hautwindow.scrollTo(0, 0); 
            /*  }  */
            toggleBodyScroll(true);
        })
        btnMenuClose.addEventListener('click', () => {
            blocnaviguation.classList.remove("activeDesactive");
            toggleBodyScroll(false);

        })

        /* ********************************** */
        const btnSearch = document.getElementById('searchbtnIcone');
        const blocSearch = document.querySelector(".blocsearch");

        btnSearch.addEventListener('click', () => {
            blocSearch.classList.toggle("activeDesactiveSearch");
        })