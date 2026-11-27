document.addEventListener("click", async event => {
  const button = event.target.closest("button[data-share]");
  if (!button) return;

  const url = new URL(button.dataset.share, window.location.href).href;
  const message = document.querySelector("#share-status");
  message.hidden = true;
  if (navigator.share) {
    try {
      await navigator.share({ title: button.dataset.shareTitle, url });
      return;
    } catch (error) {
      if (error.name === "AbortError") return;
    }
  }

  try {
    await navigator.clipboard.writeText(url);
    message.textContent = "Enlace copiado.";
    message.hidden = false;
  } catch {
    window.prompt("Copia el enlace de este recurso", url);
  }
});
