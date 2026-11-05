document.querySelectorAll("[data-image-carousel]").forEach((carousel) => {
  const slides = [...carousel.querySelectorAll(".image-carousel__slide")];
  if (slides.length < 2) return;

  let activeIndex = slides.findIndex((slide) => slide.classList.contains("is-active"));
  if (activeIndex < 0) activeIndex = 0;

  function showSlide(index) {
    slides[activeIndex].hidden = true;
    slides[activeIndex].classList.remove("is-active");
    activeIndex = (index + slides.length) % slides.length;
    slides[activeIndex].hidden = false;
    slides[activeIndex].classList.add("is-active");
  }

  carousel.querySelector("[data-carousel-previous]")?.addEventListener("click", () => {
    showSlide(activeIndex - 1);
  });
  carousel.querySelector("[data-carousel-next]")?.addEventListener("click", () => {
    showSlide(activeIndex + 1);
  });
});
