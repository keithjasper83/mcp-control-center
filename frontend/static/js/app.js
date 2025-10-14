// MCP Control Center - Main JavaScript

// Register service worker for PWA
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker
      .register('/static/pwa/service-worker.js')
      .then((registration) => {
        console.log('ServiceWorker registered:', registration);
      })
      .catch((error) => {
        console.log('ServiceWorker registration failed:', error);
      });
  });
}

// PWA install prompt
let deferredPrompt;

window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPrompt = e;
  showInstallBanner();
});

function showInstallBanner() {
  const banner = document.getElementById('install-banner');
  if (banner) {
    banner.classList.remove('hidden');
  }
}

function installPWA() {
  const banner = document.getElementById('install-banner');
  if (banner) {
    banner.classList.add('hidden');
  }

  if (deferredPrompt) {
    deferredPrompt.prompt();
    deferredPrompt.userChoice.then((choiceResult) => {
      if (choiceResult.outcome === 'accepted') {
        console.log('User accepted the install prompt');
      }
      deferredPrompt = null;
    });
  }
}

function dismissInstallBanner() {
  const banner = document.getElementById('install-banner');
  if (banner) {
    banner.classList.add('hidden');
  }
}

// Toast notifications
function showToast(message, type = 'info') {
  const toast = document.createElement('div');
  toast.className = `fixed bottom-4 right-4 p-4 rounded-lg shadow-lg ${
    type === 'success'
      ? 'bg-green-500'
      : type === 'error'
      ? 'bg-red-500'
      : 'bg-blue-500'
  } text-white z-50`;
  toast.textContent = message;

  document.body.appendChild(toast);

  setTimeout(() => {
    toast.remove();
  }, 3000);
}

// HTMX event listeners
document.body.addEventListener('htmx:afterSwap', (event) => {
  console.log('HTMX swap completed');
});

document.body.addEventListener('htmx:responseError', (event) => {
  showToast('Request failed. Please try again.', 'error');
});
