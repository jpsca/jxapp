import { Application } from "@hotwired/stimulus"

window.Stimulus = Application.start()

/* Added so the DOMContentLoaded events work without any changes. */
document.addEventListener("turbo:load", function() {
  document.dispatchEvent(new CustomEvent("DOMContentLoaded"));
});

/* Dark mode toggle */
function initDarkModeToggle() {
  const toggle = document.getElementById('dark-mode-toggle');
  if (!toggle) return;
  const html = document.documentElement;
  toggle.checked = html.classList.contains('dark');
  toggle.addEventListener('change', function() {
    html.classList.toggle('dark', toggle.checked);
    localStorage.setItem('theme', toggle.checked ? 'dark' : 'light');
  });
}

document.addEventListener("turbo:load", initDarkModeToggle);
document.addEventListener("DOMContentLoaded", initDarkModeToggle);
