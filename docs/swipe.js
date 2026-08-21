const PAIRS = {
  "2013-2025": {
    before: { src: "assets/ndvi-2013.jpg", label: "2013 NDVI" },
    after: { src: "assets/ndvi-2025.jpg", label: "2025 NDVI" },
    caption: "Pre- and post-sanctuary designation vegetation greenness",
  },
  "2013-2020": {
    before: { src: "assets/ndvi-2013.jpg", label: "2013 NDVI" },
    after: { src: "assets/ndvi-2020.jpg", label: "2020 NDVI" },
    caption: "Four years after Tatai Wildlife Sanctuary was established",
  },
  "2020-2025": {
    before: { src: "assets/ndvi-2020.jpg", label: "2020 NDVI" },
    after: { src: "assets/ndvi-2025.jpg", label: "2025 NDVI" },
    caption: "Most recent dry-season comparison",
  },
};

const shell = document.getElementById("slider-shell");
const compare = document.getElementById("compare");
const beforeImg = document.getElementById("before-img");
const afterImg = document.getElementById("after-img");
const afterWrap = document.getElementById("after-wrap");
const handle = document.getElementById("handle");
const beforeLabel = document.getElementById("before-label");
const afterLabel = document.getElementById("after-label");
const caption = document.getElementById("caption");
const tabs = document.querySelectorAll(".pair-tabs button");

let position = 50;
let dragging = false;
let activePair = "2013-2025";

function clamp(value, min, max) {
  return Math.min(max, Math.max(min, value));
}

function syncAfterImageWidth() {
  const width = compare.offsetWidth;
  afterImg.style.width = `${width}px`;
}

function setPosition(pct) {
  position = clamp(pct, 0, 100);
  afterWrap.style.width = `${position}%`;
  handle.style.left = `${position}%`;
}

function positionFromClientX(clientX) {
  const rect = compare.getBoundingClientRect();
  const x = clientX - rect.left;
  return (x / rect.width) * 100;
}

function loadPair(key) {
  const pair = PAIRS[key];
  if (!pair) return;

  activePair = key;
  beforeLabel.textContent = pair.before.label;
  afterLabel.textContent = pair.after.label;
  caption.textContent = pair.caption;

  tabs.forEach((tab) => {
    tab.classList.toggle("active", tab.dataset.pair === key);
  });

  let loaded = 0;
  const onLoad = () => {
    loaded += 1;
    if (loaded === 2) {
      syncAfterImageWidth();
      setPosition(position);
    }
  };

  beforeImg.onload = onLoad;
  afterImg.onload = onLoad;
  beforeImg.src = pair.before.src;
  afterImg.src = pair.after.src;
}

function onPointerDown(event) {
  dragging = true;
  shell.setPointerCapture(event.pointerId);
  setPosition(positionFromClientX(event.clientX));
}

function onPointerMove(event) {
  if (!dragging) return;
  setPosition(positionFromClientX(event.clientX));
}

function onPointerUp(event) {
  dragging = false;
  shell.releasePointerCapture(event.pointerId);
}

function onKeyDown(event) {
  const step = event.shiftKey ? 5 : 1;
  if (event.key === "ArrowLeft") {
    event.preventDefault();
    setPosition(position - step);
  } else if (event.key === "ArrowRight") {
    event.preventDefault();
    setPosition(position + step);
  } else if (event.key === "Home") {
    setPosition(0);
  } else if (event.key === "End") {
    setPosition(100);
  }
}

tabs.forEach((tab) => {
  tab.addEventListener("click", () => loadPair(tab.dataset.pair));
});

shell.addEventListener("pointerdown", onPointerDown);
shell.addEventListener("pointermove", onPointerMove);
shell.addEventListener("pointerup", onPointerUp);
shell.addEventListener("pointercancel", onPointerUp);
shell.addEventListener("keydown", onKeyDown);

window.addEventListener("resize", () => {
  syncAfterImageWidth();
  setPosition(position);
});

loadPair(activePair);
setPosition(50);
