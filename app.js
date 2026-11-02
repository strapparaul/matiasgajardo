'use strict';
const images = JSON.parse(document.querySelector('#gallery-data').textContent);
const viewer = document.querySelector('#viewer');
const fullImage = document.querySelector('#full-image');
const status = document.querySelector('#viewer-status');
let current = 0;
let trigger;
function renderImage(index) {
  current = index;
  const image = images[index];
  fullImage.src = image.src;
  fullImage.alt = image.title || `Obra de Matias Gajardo, imagen ${index + 1}`;
  document.querySelector('#image-title').textContent = image.title || `Obra ${index + 1}`;
  document.querySelector('#image-description').textContent = image.description || '';
  document.querySelector('#image-counter').textContent = `${index + 1} / ${images.length}`;
  document.querySelector('#image-download').href = image.src;
  status.textContent = '';
  for (const button of viewer.querySelectorAll('.previous, .next')) button.hidden = images.length < 2;
}
function syncViewer() {
  const match = /^#obra-(\d+)$/.exec(location.hash);
  const index = match ? Number(match[1]) - 1 : -1;
  if (index >= 0 && index < images.length) {
    renderImage(index);
    if (!viewer.open) viewer.showModal();
  } else if (viewer.open) viewer.close();
}
function closeViewer() {
  if (/^#obra-\d+$/.test(location.hash)) history.replaceState(null, '', location.pathname + location.search);
  viewer.close();
}
function move(delta) {
  const next = (current + delta + images.length) % images.length;
  history.replaceState(null, '', `#obra-${next + 1}`);
  renderImage(next);
}
document.querySelectorAll('[data-image]').forEach(link => {
  link.addEventListener('click', event => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    trigger = link;
    history.pushState(null, '', `#obra-${Number(link.dataset.image) + 1}`);
    syncViewer();
  });
});
viewer.querySelector('.close').addEventListener('click', closeViewer);
viewer.querySelector('.previous').addEventListener('click', () => move(-1));
viewer.querySelector('.next').addEventListener('click', () => move(1));
viewer.addEventListener('cancel', event => { event.preventDefault(); closeViewer(); });
viewer.addEventListener('close', () => trigger?.focus({ preventScroll: true }));
viewer.addEventListener('click', event => { if (event.target === viewer) closeViewer(); });
viewer.addEventListener('keydown', event => {
  if (event.target.matches('input, textarea')) return;
  if (event.key === 'ArrowRight') { event.preventDefault(); move(1); }
  if (event.key === 'ArrowLeft') { event.preventDefault(); move(-1); }
});
let touchStart;
fullImage.addEventListener('touchstart', event => { touchStart = event.touches.length === 1 ? event.touches[0].clientX : null; }, { passive: true });
fullImage.addEventListener('touchend', event => {
  if (touchStart === null || event.changedTouches.length !== 1) return;
  const delta = event.changedTouches[0].clientX - touchStart;
  if (Math.abs(delta) > 60) move(delta < 0 ? 1 : -1);
  touchStart = null;
}, { passive: true });
document.querySelector('#copy-link').addEventListener('click', async () => {
  try {
    await navigator.clipboard.writeText(location.href);
    status.textContent = 'Enlace copiado.';
  } catch {
    status.textContent = 'Copia el enlace de la barra de direcciones para compartir esta imagen.';
  }
});
window.addEventListener('hashchange', syncViewer);
window.addEventListener('popstate', syncViewer);
syncViewer();
const contactForm = document.querySelector('#contact-form');
contactForm?.addEventListener('submit', event => {
  event.preventDefault();
  const values = new FormData(contactForm);
  const body = `${values.get('message')}\n\n${values.get('name')}\n${values.get('email')}`;
  location.href = `mailto:matiasgajardo.correo@gmail.com?subject=${encodeURIComponent(values.get('subject'))}&body=${encodeURIComponent(body)}`;
  document.querySelector('#form-status').textContent = 'Continúa en tu aplicación de correo para enviar el mensaje. También puedes escribir a matiasgajardo.correo@gmail.com.';
});
const navigation = document.querySelector('.navigation');
const desktopNavigation = window.matchMedia('(min-width: 1001px)');
function resizeNavigation() { navigation.open = desktopNavigation.matches; }
resizeNavigation();
desktopNavigation.addEventListener('change', resizeNavigation);
