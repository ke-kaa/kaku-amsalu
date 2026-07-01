(() => {
  const track = document.getElementById('track');
  const panels = Array.from(track.querySelectorAll('.panel'));
  const counter = document.getElementById('counter');
  const progressBar = document.getElementById('progressBar');
  const nextBtn = document.getElementById('nextBtn');
  const prevBtn = document.getElementById('prevBtn');
  const indexBtn = document.getElementById('indexBtn');
  const overlay = document.getElementById('overlay');
  const overlayClose = document.getElementById('overlayClose');
  const overlayList = document.getElementById('overlayList');
  const clockEl = document.getElementById('clock');
  const total = panels.length;

  /* ── Build index overlay ── */
  panels.forEach((p, i) => {
    const a = document.createElement('a');
    a.href = '#';
    const num = String(i).padStart(2, '0');
    const label = p.dataset.label || '—';
    a.innerHTML = `<span class="num">${num}</span><span class="lbl">${label}</span><span class="arr">→</span>`;
    a.addEventListener('click', (e) => {
      e.preventDefault();
      goTo(i);
      closeOverlay();
    });
    overlayList.appendChild(a);
  });

  /* ── Active panel detection ── */
  const io = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && entry.intersectionRatio > 0.55) {
        const idx = panels.indexOf(entry.target);
        setActive(idx);
      }
    });
  }, { root: track, threshold: [0, 0.25, 0.55, 0.9] });
  panels.forEach(p => io.observe(p));

  let activeIdx = 0;
  function setActive(i){
    if (i === activeIdx) return;
    activeIdx = i;
    panels.forEach((p, idx) => p.classList.toggle('active', idx === i));
    counter.textContent = String(i+1).padStart(2,'0') + ' / ' + String(total).padStart(2,'0');
    progressBar.style.setProperty('--progress', ((i)/(total-1) * 100) + '%');
    prevBtn.disabled = i === 0;
    nextBtn.disabled = i === total - 1;
  }
  // initialize
  panels[0].classList.add('active');
  setActive(0);
  // Force initial update of vars
  requestAnimationFrame(() => {
    counter.textContent = '01 / ' + String(total).padStart(2,'0');
    progressBar.style.setProperty('--progress', '0%');
  });

  /* ── Navigation ── */
  function goTo(i){
    i = Math.max(0, Math.min(total - 1, i));
    track.scrollTo({ left: i * window.innerWidth, behavior: 'smooth' });
  }
  nextBtn.addEventListener('click', () => goTo(activeIdx + 1));
  prevBtn.addEventListener('click', () => goTo(activeIdx - 1));

  /* ── Wheel: convert vertical → horizontal ── */
  let wheelLock = false;
  track.addEventListener('wheel', (e) => {
    // If user is using a touchpad with horizontal intent, let it pass.
    if (Math.abs(e.deltaX) > Math.abs(e.deltaY)) return;
    e.preventDefault();
    // Snap-step on each wheel impulse (debounced)
    if (wheelLock) return;
    if (Math.abs(e.deltaY) < 8) return;
    wheelLock = true;
    if (e.deltaY > 0) goTo(activeIdx + 1);
    else goTo(activeIdx - 1);
    setTimeout(() => { wheelLock = false; }, 700);
  }, { passive: false });

  /* ── Keyboard ── */
  window.addEventListener('keydown', (e) => {
    if (overlay.classList.contains('open')){
      if (e.key === 'Escape') closeOverlay();
      return;
    }
    if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' '){
      e.preventDefault(); goTo(activeIdx + 1);
    } else if (e.key === 'ArrowLeft' || e.key === 'PageUp'){
      e.preventDefault(); goTo(activeIdx - 1);
    } else if (e.key === 'Home'){
      e.preventDefault(); goTo(0);
    } else if (e.key === 'End'){
      e.preventDefault(); goTo(total - 1);
    } else if (e.key.toLowerCase() === 'i'){
      openOverlay();
    }
  });

  /* ── Touch: swipe left/right ── */
  let touchStartX = 0, touchStartY = 0, touched = false;
  track.addEventListener('touchstart', (e) => {
    touchStartX = e.touches[0].clientX;
    touchStartY = e.touches[0].clientY;
    touched = true;
  }, { passive: true });
  track.addEventListener('touchend', (e) => {
    if (!touched) return;
    touched = false;
    const dx = e.changedTouches[0].clientX - touchStartX;
    const dy = e.changedTouches[0].clientY - touchStartY;
    if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy)){
      if (dx < 0) goTo(activeIdx + 1);
      else goTo(activeIdx - 1);
    }
  });

  /* ── Resize: keep snapped to current panel ── */
  let resizeT;
  window.addEventListener('resize', () => {
    clearTimeout(resizeT);
    resizeT = setTimeout(() => {
      track.scrollTo({ left: activeIdx * window.innerWidth, behavior: 'auto' });
    }, 120);
  });

  /* ── Overlay ── */
  function openOverlay(){ overlay.classList.add('open'); }
  function closeOverlay(){ overlay.classList.remove('open'); }
  indexBtn.addEventListener('click', openOverlay);
  overlayClose.addEventListener('click', closeOverlay);

  /* ── Build calendar grid for Timesheet frame ── */
  const cal = document.getElementById('calGrid');
  if (cal){
    const states = [
      'on','on','on','partial','on','',  '',
      'on','on','on','on','on','partial','',
      'on','on','partial','on','on','',  '',
      'on','on','on','on','on','partial','',
    ];
    states.forEach(s => {
      const c = document.createElement('div');
      c.className = 'cell' + (s ? ' ' + s : '');
      cal.appendChild(c);
    });
  }

  /* ── Clock (Africa/Addis_Ababa) ── */
  function tick(){
    const d = new Date();
    // EAT is UTC+3
    const eat = new Date(d.getTime() + (d.getTimezoneOffset() + 180) * 60000);
    const hh = String(eat.getHours()).padStart(2,'0');
    const mm = String(eat.getMinutes()).padStart(2,'0');
    const ss = String(eat.getSeconds()).padStart(2,'0');
    clockEl.textContent = 'EAT — ' + hh + ':' + mm + ':' + ss;
  }
  tick(); setInterval(tick, 1000);

})();
