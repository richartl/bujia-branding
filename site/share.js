async function copyText(value, success, fallback) {
  const message = document.querySelector("#action-status");
  try {
    await navigator.clipboard.writeText(value);
    message.textContent = success;
    message.hidden = false;
  } catch {
    window.prompt(fallback, value);
  }
}

document.addEventListener("click", async event => {
  const button = event.target.closest("button[data-share], button[data-copy-code]");
  if (!button) return;

  document.querySelector("#action-status").hidden = true;
  if (button.dataset.copyCode) {
    await copyText(button.dataset.copyCode, "Código copiado.", "Copia el código de esta imagen");
    return;
  }

  const url = new URL(button.dataset.share, window.location.href).href;
  if (navigator.share) {
    try {
      await navigator.share({ title: button.dataset.shareTitle, url });
      return;
    } catch (error) {
      if (error.name === "AbortError") return;
    }
  }

  await copyText(url, "Enlace copiado.", "Copia el enlace de este recurso");
});
