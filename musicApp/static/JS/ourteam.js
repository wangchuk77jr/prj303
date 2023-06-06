const prevBtn = document.querySelector('#prevBtn');
const nextBtn = document.querySelector('#nextBtn');
const scrollArea = document.querySelector('.ourteam .row');

// add event listeners to the previous and next buttons
prevBtn.addEventListener('click', () => {
  scrollArea.scrollBy({ left: -300, behavior: 'smooth' });
});

nextBtn.addEventListener('click', () => {
  scrollArea.scrollBy({ left: 300, behavior: 'smooth' });
});

