const data = window.catalog;
const search = document.querySelector("#search");
const status = document.querySelector("#status");
const catalog = document.querySelector("#catalog");
const nav = document.querySelector("#categories");
const results = document.querySelector("#results");
const template = document.querySelector("#card");
const stateLabels = { approved: "Aprobado", review: "En revisión", draft: "Borrador", archived: "Archivado", rejected: "Rechazado" };
const normalize = value => value.normalize("NFD").replace(/\p{Diacritic}/gu, "").toLowerCase();
const merch = new Set(["t-shirts", "totebags", "caps", "merch"]);
let category = "";

document.querySelector(".controls").addEventListener("submit", event => event.preventDefault());
search.addEventListener("input", render);
status.addEventListener("change", render);

for (const [key, label] of [["", "Todos"], ["all-merch", "Merch"], ...data.categories]) {
  const button = document.createElement("button");
  button.type = "button";
  button.textContent = label;
  button.dataset.category = key;
  button.addEventListener("click", () => { category = key; render(); });
  nav.append(button);
}

function matchesCategory(key) {
  return !category || (category === "all-merch" ? merch.has(key) : category === key);
}

function render() {
  const terms = normalize(search.value).trim().split(/\s+/);
  const matches = data.items.filter(item => {
    const words = normalize([item.title, item.description, item.id, item.categoryLabel, item.version].join(" "));
    return matchesCategory(item.category) && (!status.value || item.status === status.value)
      && terms.every(term => words.includes(term));
  });

  for (const button of nav.children) {
    button.setAttribute("aria-pressed", String(button.dataset.category === category));
  }
  results.textContent = matches.length === 1 ? "1 recurso" : `${matches.length} recursos`;
  catalog.replaceChildren();
  for (const [key, label] of data.categories) {
    if (!matchesCategory(key)) continue;
    const items = matches.filter(item => item.category === key);
    if (!items.length) continue;
    const section = document.createElement("section");
    const heading = document.createElement("h2");
    heading.textContent = label;
    const grid = document.createElement("div");
    grid.className = "grid";
    for (const item of items) grid.append(cardFor(item));
    section.append(heading, grid);
    catalog.append(section);
  }
  if (!matches.length) {
    const message = document.createElement("p");
    message.textContent = "No hay recursos que coincidan con la selección.";
    catalog.append(message);
  }
}

function cardFor(item) {
  const fragment = template.content.cloneNode(true);
  const preview = fragment.querySelector(".preview");
  const state = fragment.querySelector(".state");
  preview.href = item.file;
  preview.setAttribute("aria-label", `Abrir ${item.title}`);
  if (item.thumbnail) {
    const image = new Image();
    image.loading = "lazy";
    image.src = item.thumbnail;
    image.alt = item.title;
    preview.append(image);
  } else {
    preview.textContent = item.format;
  }
  state.dataset.status = item.status;
  state.textContent = stateLabels[item.status] ?? item.status;
  fragment.querySelector(".version").textContent = `v${item.version}`;
  fragment.querySelector("h3").textContent = item.title;
  fragment.querySelector("p").textContent = item.description;
  fragment.querySelector(".file").href = item.file;
  fragment.querySelector(".record").href = item.card;
  return fragment;
}

render();
