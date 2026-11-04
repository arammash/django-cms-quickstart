document.addEventListener("click", (event) => {
  const toggle = event.target.closest(".nav-dropdown-toggle");
  if (!toggle) {
    document.querySelectorAll(".nav-dropdown-toggle[aria-expanded='true']").forEach((openToggle) => {
      openToggle.setAttribute("aria-expanded", "false");
      openToggle.closest(".has-dropdown").classList.remove("dropdown-open");
    });
    return;
  }

  const isExpanded = toggle.getAttribute("aria-expanded") === "true";
  toggle.setAttribute("aria-expanded", String(!isExpanded));
  toggle.closest(".has-dropdown").classList.toggle("dropdown-open", !isExpanded);
});

const exhibitionColumns = document.querySelectorAll(".exhibition-column");

function filterExhibitionColumns() {
  const selectedId = window.location.hash.slice(1);
  const hasSelection = ["past", "current", "future"].includes(selectedId);

  exhibitionColumns.forEach((column) => {
    const isSelected = !hasSelection || column.id === selectedId;
    column.setAttribute("aria-hidden", String(!isSelected));
    column.inert = !isSelected;
  });
}

if (exhibitionColumns.length) {
  window.addEventListener("hashchange", filterExhibitionColumns);
  filterExhibitionColumns();
}
