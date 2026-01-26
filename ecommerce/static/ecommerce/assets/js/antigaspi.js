(function(){
    
    const track = document.getElementById('slidesTrack');
    const slides = document.querySelectorAll('.slide');
    const navBars = document.querySelectorAll('.nav-bar');
    let currentSlide = 0;
    const maxIndex = slides.length - 1;
    let isPaused = false; 

    function updateUI(index){
        if(!track) return;
        track.style.transition = 'transform 350ms ease';
        track.style.transform = 'translateX(-' + (index * 100) + '%)';
        navBars.forEach(bar => bar.classList.remove('active'));
        if(navBars[index]) navBars[index].classList.add('active');
    }

    window.goToSlide = function(index){
        if(index < 0) index = 0;
        if(index > maxIndex) index = maxIndex;
        currentSlide = index;
        updateUI(index);
    }

    window.nextSlide = function(){
        currentSlide = (currentSlide >= maxIndex) ? 0 : currentSlide + 1;
        updateUI(currentSlide);
    }

    window.prevSlide = function(){
        currentSlide = (currentSlide <= 0) ? maxIndex : currentSlide - 1;
        updateUI(currentSlide);
    }

    
    if(track) updateUI(currentSlide);

    const AUTOPLAY_DELAY = 5000;
    let autoplayTimer = null;

    function startAutoplay(){
        stopAutoplay();
        autoplayTimer = setInterval(()=>{
            if(!isPaused) nextSlide();
        }, AUTOPLAY_DELAY);
    }
    function stopAutoplay(){
        if(autoplayTimer){ clearInterval(autoplayTimer); autoplayTimer = null; }
    }

    const sliderContainer = document.querySelector('.sauveplat-slider-container');
    if(sliderContainer){
        sliderContainer.addEventListener('mouseenter', ()=> { isPaused = true; });
        sliderContainer.addEventListener('mouseleave', ()=> { isPaused = false; });
        sliderContainer.addEventListener('focusin', ()=> { isPaused = true; });
        sliderContainer.addEventListener('focusout', ()=> { isPaused = false; });
    }
    
    navBars.forEach((bar, i) => {
        bar.addEventListener('click', () => { window.goToSlide(i); isPaused = true; });
        bar.addEventListener('keydown', (e)=> { if(e.key === 'Enter'){ window.goToSlide(i); isPaused = true; } });
    });

    const leftArrow = document.querySelector('.slider-arrow.left');
    const rightArrow = document.querySelector('.slider-arrow.right');
    if(leftArrow){ leftArrow.addEventListener('click', ()=>{ prevSlide(); isPaused = true; }); }
    if(rightArrow){ rightArrow.addEventListener('click', ()=>{ nextSlide(); isPaused = true; }); }
    
    document.addEventListener('keydown', function(e){
        if(e.key === 'ArrowRight') { nextSlide(); isPaused = true; }
        if(e.key === 'ArrowLeft') { prevSlide(); isPaused = true; }
    });

    // Touch events pour le slider
    if(track) {
        let touchStartX = 0;
        let touchDeltaX = 0;
        let isTouching = false;

        track.addEventListener('touchstart', (e) => {
            if(e.touches && e.touches.length === 1){
                isTouching = true;
                touchStartX = e.touches[0].clientX;
                touchDeltaX = 0;
                isPaused = true;
                track.style.transition = 'none';
            }
        }, {passive:true});

        track.addEventListener('touchmove', (e) => {
            if(!isTouching) return;
            touchDeltaX = e.touches[0].clientX - touchStartX;
            const percent = (touchDeltaX / track.offsetWidth) * 100;
            track.style.transform = 'translateX(' + ( -currentSlide * 100 + -percent ) + '%)';
            e.preventDefault();
        }, {passive:false});

        track.addEventListener('touchend', (e) => {
            if(!isTouching) return;
            isTouching = false;
            track.style.transition = 'transform 300ms ease';
            const threshold = 50; 
            if(Math.abs(touchDeltaX) > threshold){
                if(touchDeltaX < 0) { nextSlide(); } else { prevSlide(); }
            } else {
                updateUI(currentSlide);
            }
            setTimeout(()=>{ isPaused = false; }, 1500);
        }, {passive:true});
    }

    startAutoplay();



    function applyTheme(){
        var hour = new Date().getHours();
        var isNight = (hour < 7 || hour >= 18); 
        var root = document.documentElement;
        root.classList.remove('light-theme','dark-theme');
        root.classList.add(isNight ? 'dark-theme' : 'light-theme');
    }
    
    const yearSpan = document.getElementById('year-footer');
    if(yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }

    applyTheme();
    setInterval(applyTheme, 60 * 1000);

})();