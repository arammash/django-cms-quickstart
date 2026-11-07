(() => {
  const exhibitionButtons = document.querySelectorAll(".past-exhibition-button");
  const artistNames = document.querySelectorAll(".other-artist-list [data-artist-id]");

  exhibitionButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const alreadySelected = button.getAttribute("aria-pressed") === "true";
      exhibitionButtons.forEach((item) => item.setAttribute("aria-pressed", "false"));

      if (alreadySelected) {
        artistNames.forEach((artist) => artist.classList.remove("is-highlighted"));
        return;
      }

      button.setAttribute("aria-pressed", "true");
      const artistIds = new Set(button.dataset.artistIds.split(",").filter(Boolean));
      artistNames.forEach((artist) => {
        artist.classList.toggle("is-highlighted", artistIds.has(artist.dataset.artistId));
      });
    });
  });
})();
