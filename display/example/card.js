function onCardClick() {
  const msg = document.getElementById("card-message");
  msg.classList.toggle("hidden");
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelector('[data-card-btn]').addEventListener('click', onCardClick);
});
