document.querySelector('.menu-btn')?.addEventListener('click', () => document.querySelector('#navlinks').classList.toggle('open'));
document.querySelectorAll('.faq-q').forEach(button => button.addEventListener('click', () => button.parentElement.classList.toggle('open')));
document.querySelectorAll('[data-lightbox]').forEach(button => button.addEventListener('click', () => {
  const box = document.createElement('div');
  box.className = 'lightbox';
  const close = document.createElement('button'); close.textContent = '×'; close.setAttribute('aria-label', 'Sluiten');
  const image = document.createElement('img'); image.src = button.dataset.lightbox; image.alt = button.querySelector('img')?.alt || 'Galerijfoto';
  box.append(close, image); close.addEventListener('click', () => box.remove()); box.addEventListener('click', event => { if (event.target === box) box.remove(); });
  document.body.append(box);
}));
