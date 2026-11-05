(() => {
  const links = document.querySelectorAll(".artist-list a");

  function showPreview(link, x, y) {
    const image = link.querySelector(".artist-hover-image");
    if (!image) return;

    image.classList.add("is-visible");
    const bounds = image.getBoundingClientRect();
    const gap = 12;
    let left = x + gap;
    let top = y + gap;

    if (left + bounds.width > window.innerWidth - 8) {
      left = x - bounds.width - gap;
    }
    if (top + bounds.height > window.innerHeight - 8) {
      top = window.innerHeight - bounds.height - 8;
    }

    image.style.left = `${Math.max(8, left)}px`;
    image.style.top = `${Math.max(8, top)}px`;
  }

  function hidePreview(link) {
    link.querySelector(".artist-hover-image")?.classList.remove("is-visible");
  }

  links.forEach((link) => {
    link.addEventListener("pointerenter", (event) => {
      if (event.pointerType === "mouse" || event.pointerType === "pen") {
        showPreview(link, event.clientX, event.clientY);
      }
    });
    link.addEventListener("pointermove", (event) => {
      if (event.pointerType === "mouse" || event.pointerType === "pen") {
        showPreview(link, event.clientX, event.clientY);
      }
    });
    link.addEventListener("pointerleave", () => hidePreview(link));
    link.addEventListener("focus", () => {
      const bounds = link.getBoundingClientRect();
      showPreview(link, bounds.left + bounds.width / 2, bounds.top + bounds.height / 2);
    });
    link.addEventListener("blur", () => hidePreview(link));
  });
})();
