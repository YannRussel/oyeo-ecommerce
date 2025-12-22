    document.querySelectorAll('.product-carousel-wrapper').forEach(wrapper => {
      const slider = wrapper.querySelector('.product-grid');
      let isDown = false, startX, scrollLeft, velocity = 0, momentumID;

      // Drag & scroll
      slider.addEventListener('mousedown', e => {
        isDown = true;
        startX = e.pageX - slider.offsetLeft;
        scrollLeft = slider.scrollLeft;
        cancelMomentumTracking();
      });

      slider.addEventListener('mouseleave', () => {
        if (!isDown) return;
        isDown = false;
        beginMomentumTracking();
      });

      slider.addEventListener('mouseup', () => {
        isDown = false;
        beginMomentumTracking();
      });

      slider.addEventListener('mousemove', e => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.pageX - slider.offsetLeft;
        const walk = (x - startX) * 1.5;
        const prev = slider.scrollLeft;
        slider.scrollLeft = scrollLeft - walk;
        velocity = slider.scrollLeft - prev;
      });

      function beginMomentumTracking() {
        cancelMomentumTracking();
        momentumID = requestAnimationFrame(momentumLoop);
      }

      function cancelMomentumTracking() {
        cancelAnimationFrame(momentumID);
      }

      function momentumLoop() {
        slider.scrollLeft += velocity;
        velocity *= 0.95;
        if (Math.abs(velocity) > 0.5) {
          momentumID = requestAnimationFrame(momentumLoop);
        }
      }

      // Flèches
      wrapper.querySelectorAll('.scroll-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          cancelMomentumTracking();
          const direction = btn.classList.contains('left') ? -1 : 1;
          const cardWidth = slider.querySelector('.product-card').offsetWidth + 16;
          slider.scrollBy({ left: direction * cardWidth, behavior: 'smooth' });
        });
      });
    });
