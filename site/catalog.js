const data = window.catalog;
const search = document.querySelector("#search");
const catalog = document.querySelector("#catalog");
const nav = document.querySelector("#categories");
const results = document.querySelector("#results");
const template = document.querySelector("#card");
const normalize = value => value.normalize("NFD").replace(/\p{Diacritic}/gu, "").toLowerCase();
const merch = new Set(["t-shirts", "totebags", "caps", "merch"]);
let category = "";

document.querySelector(".controls").addEventListener("submit", event => event.preventDefault());
search.addEventListener("input", render);

const filters = [["", "Todos"], ...data.categories];
if (data.categories.some(([key]) => merch.has(key))) filters.splice(1, 0, ["all-merch", "Merch"]);
for (const [key, label] of filters) {
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
    return matchesCategory(item.category) && terms.every(term => words.includes(term));
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
  preview.href = item.page;
  preview.setAttribute("aria-label", `Ver detalles de ${item.title}`);
  if (item.thumbnail) {
    const image = new Image();
    image.loading = "lazy";
    image.src = item.thumbnail;
    image.alt = item.title;
    preview.append(image);
  } else {
    preview.textContent = item.format;
  }
  state.dataset.status = "approved";
  state.textContent = "Aprobado";
  fragment.querySelector(".version").textContent = `v${item.version}`;
  const record = fragment.querySelector(".record");
  record.textContent = item.title;
  record.href = item.page;
  fragment.querySelector("p").textContent = item.description;
  fragment.querySelector(".file").href = item.file;
  const share = fragment.querySelector("[data-share]");
  share.dataset.share = item.page;
  share.dataset.shareTitle = item.title;
  return fragment;
}

render();
