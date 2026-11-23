/**
 * SpeechBloom AI — Core JS Utilities v2
 * Shared across all pages: API calls, auth state, toast, session helpers
 */

// ── API CALL ──────────────────────────────────────────────
async function apiCall(url, method = 'GET', body = null) {
  const opts = {
    method,
    headers: { 'Content-Type': 'application/json' },
    credentials: 'same-origin'
  };
  if (body && method !== 'GET') opts.body = JSON.stringify(body);
  const res = await fetch(url, opts);
  const data = await res.json();
  if (!res.ok) throw new Error(data.message || `Request failed (${res.status})`);
  return data;
}

// ── TOAST NOTIFICATIONS ──────────────────────────────────
function ensureToastContainer() {
  let c = document.getElementById('toast-container');
  if (!c) {
    c = document.createElement('div');
    c.id = 'toast-container';
    c.className = 'toast-container';
    document.body.appendChild(c);
  }
  return c;
}

function showToast(message, type = 'info', duration = 4000) {
  const container = ensureToastContainer();
  const icons = { success: '✅', error: '❌', warn: '⚠️', info: 'ℹ️' };
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `<span>${icons[type] || 'ℹ️'}</span><span>${message}</span>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.transition = 'all 0.3s ease';
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(60px)';
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

// Legacy showAlert wrapper (some pages use this)
function showAlert(message, type = 'info', targetId = 'alert-box') {
  const el = document.getElementById(targetId);
  if (el) {
    const alertType = type === 'error' ? 'alert-error' : type === 'success' ? 'alert-success' : 'alert-info';
    el.innerHTML = `<div class="alert ${alertType}">${message}</div>`;
    setTimeout(() => { el.innerHTML = ''; }, 4500);
    // Only show toast if there's NO visible alert-box in the page
    return;
  }
  // No alert-box found — fall back to toast
  showToast(message, type === 'error' ? 'error' : type === 'success' ? 'success' : 'info');
}

// ── CHILD SESSION ─────────────────────────────────────────
function getSelectedChildId()   { return localStorage.getItem('sb_child_id') || null; }
function setSelectedChildId(id) { localStorage.setItem('sb_child_id', String(id)); }
function clearSelectedChild()   { localStorage.removeItem('sb_child_id'); localStorage.removeItem('sb_child_name'); localStorage.removeItem('sb_child_avatar'); }

function getChildName()   { return localStorage.getItem('sb_child_name') || 'Child'; }
function getChildAvatar() { return localStorage.getItem('sb_child_avatar') || '🧒'; }

function setChildContext(id, name, avatar) {
  localStorage.setItem('sb_child_id', String(id));
  localStorage.setItem('sb_child_name', name);
  localStorage.setItem('sb_child_avatar', avatar || '🧒');
}

// ── NAV BADGE ─────────────────────────────────────────────
// Only show the active-child badge when the user is inside the child dashboard.
// On all other pages (home, profile, parent dashboard, etc.) hide it so stale
// localStorage values from a previous session never bleed through.
function updateNavChildBadge() {
  const badge = document.getElementById('nav-child-badge');
  if (!badge) return;

  const path = window.location.pathname;
  const isChildSession = path.startsWith('/dashboard/') || path.startsWith('/recording/');

  if (isChildSession && getSelectedChildId()) {
    badge.style.display = 'flex';
    badge.querySelector('.avatar').textContent     = getChildAvatar();
    badge.querySelector('.child-name').textContent = getChildName();
  } else {
    badge.style.display = 'none';
  }
}

// ── PROTECTION: CHILD-REQUIRED PAGES ─────────────────────
function requireChildSelected(redirectTo = '/profile/') {
  if (!getSelectedChildId()) {
    showToast('Please select a child profile first.', 'warn');
    setTimeout(() => { window.location.href = redirectTo; }, 800);
    return false;
  }
  return true;
}

// ── ACTIVE NAV LINK ───────────────────────────────────────
function setActiveNavLink() {
  const path = window.location.pathname;
  document.querySelectorAll('.nav-links a').forEach(a => {
    a.classList.remove('active');
    const href = a.getAttribute('href');
    if (href && href !== '/' && path.startsWith(href)) a.classList.add('active');
    if (href === '/' && path === '/') a.classList.add('active');
  });
}

// ── MOBILE NAV ────────────────────────────────────────────
function initMobileNav() {
  const burger = document.getElementById('nav-burger');
  const navLinks = document.querySelector('.nav-links');
  if (!burger || !navLinks) return;
  burger.addEventListener('click', () => {
    navLinks.classList.toggle('open');
    burger.setAttribute('aria-expanded', navLinks.classList.contains('open'));
  });
  document.addEventListener('click', e => {
    if (!burger.contains(e.target) && !navLinks.contains(e.target)) {
      navLinks.classList.remove('open');
    }
  });
}

// ── TTS ───────────────────────────────────────────────────
function speakWord(word, language = 'english') {
  if (!('speechSynthesis' in window)) return;
  window.speechSynthesis.cancel();
  const utt = new SpeechSynthesisUtterance(word);
  utt.lang  = language.toLowerCase() === 'hindi' ? 'hi-IN' : 'en-US';
  utt.rate  = 0.82;
  window.speechSynthesis.speak(utt);
}

// ── PAGE LOAD ─────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  setActiveNavLink();
  updateNavChildBadge();
  initMobileNav();
});
