document.addEventListener('DOMContentLoaded', () => {
    const carouselContainer = document.getElementById('product-carousel');
    const items = carouselContainer.querySelectorAll('.carousel-item');
    const pipsContainer = document.getElementById('carousel-pips');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');

    let currentIndex = 0;

    if (items.length === 0) {
        prevBtn.style.display = 'none';
        nextBtn.style.display = 'none';
        return;
    }

    items.forEach((_, index) => {
        const pip = document.createElement('button');
        pip.classList.add('carousel-pip');
        pip.ariaLabel = `Go to slide ${index + 1}`;
        
        pip.addEventListener('click', () => {
            currentIndex = index;
            updateCarousel();
        });
        
        pipsContainer.appendChild(pip);
    });

    const pips = pipsContainer.querySelectorAll('.carousel-pip');

    function updateCarousel() {
        items.forEach((item, index) => {
            if (index === currentIndex) {
                item.classList.add('active');
                item.style.display = 'block'; 
            } else {
                item.classList.remove('active');
                item.style.display = 'none';
            }
        });

        pips.forEach((pip, index) => {
            if (index === currentIndex) {
                pip.classList.add('active');
            } else {
                pip.classList.remove('active');
            }
        });
    }

    nextBtn.addEventListener('click', (e) => {
        e.preventDefault();
        currentIndex = (currentIndex + 1) % items.length;
        updateCarousel();
    });

    prevBtn.addEventListener('click', (e) => {
        e.preventDefault();
        currentIndex = (currentIndex - 1 + items.length) % items.length;
        updateCarousel();
    });

    updateCarousel();
});
