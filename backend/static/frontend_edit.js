(() => {
  const dialog = document.getElementById("frontend-edit-dialog");
  if (!dialog) return;

  const frame = dialog.querySelector("iframe");
  let pendingNavigation;

  document.addEventListener(
    "click",
    (event) => {
      const editable = event.target.closest("[data-frontend-edit-url]");
      const link = event.target.closest("a");
      if (!editable || !link || !editable.contains(link)) return;
      if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;

      event.preventDefault();
      window.clearTimeout(pendingNavigation);
      pendingNavigation = window.setTimeout(() => {
        window.location.assign(link.href);
      }, 250);
    },
    true,
  );

  document.addEventListener("dblclick", (event) => {
    const editable = event.target.closest("[data-frontend-edit-url]");
    if (!editable) return;

    window.clearTimeout(pendingNavigation);
    event.preventDefault();
    frame.src = editable.dataset.frontendEditUrl;
    dialog.showModal();
  });

  dialog.addEventListener("click", (event) => {
    if (event.target === dialog || event.target.closest("[data-close-frontend-editor]")) {
      dialog.close();
    }
  });

  dialog.addEventListener("close", () => {
    frame.src = "about:blank";
  });
})();
