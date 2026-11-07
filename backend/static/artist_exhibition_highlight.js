(() => {
  const exhibitionButtons = document.querySelectorAll(".past-exhibition-button");
  const clearButton = document.querySelector(".past-exhibition-clear");
  const artistEntries = document.querySelectorAll(
    ".artist-list [data-artist-id], .other-artist-list [data-artist-id]",
  );

  const clearSelection = () => {
    exhibitionButtons.forEach((button) => button.setAttribute("aria-pressed", "false"));
    artistEntries.forEach((artist) => artist.classList.remove("is-highlighted"));
  };

  exhibitionButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const alreadySelected = button.getAttribute("aria-pressed") === "true";
      if (alreadySelected) {
        clearSelection();
        return;
      }

      exhibitionButtons.forEach((item) => item.setAttribute("aria-pressed", "false"));
      button.setAttribute("aria-pressed", "true");
      const artistIds = new Set(button.dataset.artistIds.split(",").filter(Boolean));
      artistEntries.forEach((artist) => {
        artist.classList.toggle("is-highlighted", artistIds.has(artist.dataset.artistId));
      });
    });
  });

  clearButton?.addEventListener("click", clearSelection);
})();
