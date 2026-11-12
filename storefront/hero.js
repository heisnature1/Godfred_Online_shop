(() => {
  const model = document.getElementById('hero-shoe');
  const stage = document.getElementById('hero-stage');
  const controls = document.getElementById('hero-controls');
  const toggle = document.querySelector('.motion-toggle');
  const swatches = document.querySelectorAll('.swatch');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let rotating = !reducedMotion.matches;

  function setRotation(enabled) {
    rotating = enabled;
    model.autoRotate = rotating;
    toggle.setAttribute('aria-pressed', String(rotating));
    toggle.textContent = rotating ? 'Pause rotation' : 'Play rotation';
  }
  setRotation(rotating);
  model.addEventListener('load', () => {
    stage.classList.add('model-loaded');
    controls.hidden = false;
    model.variantName = 'midnight';
  });
  model.addEventListener('error', () => {
    stage.classList.remove('model-loaded');
    controls.hidden = true;
  });
  toggle.addEventListener('click', () => setRotation(!rotating));
  swatches.forEach(button => button.addEventListener('click', () => {
    model.variantName = button.dataset.variant;
    swatches.forEach(swatch => swatch.setAttribute('aria-pressed', String(swatch === button)));
  }));
  reducedMotion.addEventListener('change', event => {
    if (event.matches) setRotation(false);
  });
})();
