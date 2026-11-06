type Shoe = {
  id: string;
  brand: string;
  model: string;
  colorway: string;
  category: string;
  price: number;
  currency: string;
  purchaseYear: number;
  wornSince?: number;
  rating: number;
  comments: string;
  details: string[];
  imageUrl?: string;
};

const app = document.querySelector<HTMLDivElement>("#app");

if (!app) {
  throw new Error("The app root element is missing.");
}

const formatPrice = (shoe: Shoe): string =>
  new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: shoe.currency,
  }).format(shoe.price);

const shoeImage = (shoe: Shoe, className: string): string => `
  <div class="${className} ${className}--${shoe.id} ${shoe.imageUrl ? "" : "shoe-image--placeholder"}">
    ${shoe.imageUrl
      ? `<img src="${shoe.imageUrl}" alt="${shoe.brand} ${shoe.model}" draggable="false" />`
      : `<span>${shoe.brand}</span>`}
  </div>
`;

const renderDetail = (shoe: Shoe): string => `
  <section class="detail" aria-label="${shoe.brand} ${shoe.model}">
    <button class="close-button" type="button" aria-label="Close details">×</button>
    ${shoeImage(shoe, "detail__image")}
    <div class="detail__content">
      <p class="eyebrow">${shoe.brand} · ${shoe.category}</p>
      <h1>${shoe.model}</h1>
      <p class="detail__colorway">${shoe.colorway}</p>
      <p class="detail__comment">“${shoe.comments}”</p>
      <dl>
        <div><dt>Price</dt><dd>${formatPrice(shoe)}</dd></div>
        <div><dt>Purchased</dt><dd>${shoe.purchaseYear}</dd></div>
        ${shoe.wornSince ? `<div><dt>Worn since</dt><dd>${shoe.wornSince}</dd></div>` : ""}
        <div><dt>Rating</dt><dd>★ ${shoe.rating}</dd></div>
      </dl>
      <ul class="detail__tags">${shoe.details.map((detail) => `<li>${detail}</li>`).join("")}</ul>
    </div>
  </section>
`;

const enableDragging = (carousel: HTMLElement): void => {
  let isDragging = false;
  let startX = 0;
  let startScrollLeft = 0;

  carousel.addEventListener("pointerdown", (event) => {
    isDragging = true;
    startX = event.clientX;
    startScrollLeft = carousel.scrollLeft;
    carousel.classList.add("is-dragging");
    carousel.setPointerCapture(event.pointerId);
  });
  carousel.addEventListener("pointermove", (event) => {
    if (isDragging) carousel.scrollLeft = startScrollLeft - (event.clientX - startX);
  });

  const stopDragging = (): void => {
    isDragging = false;
    carousel.classList.remove("is-dragging");
  };
  carousel.addEventListener("pointerup", stopDragging);
  carousel.addEventListener("pointercancel", stopDragging);
  carousel.addEventListener("pointerleave", stopDragging);
};

const render = (shoes: Shoe[]): void => {
  app.innerHTML = `
    <main class="showcase">
      <section class="carousel" aria-label="Shoe collection">
        ${shoes.map((shoe) => `
          <button class="shoe" type="button" data-shoe-id="${shoe.id}" aria-label="View ${shoe.brand} ${shoe.model}">
            ${shoeImage(shoe, "shoe__image")}
          </button>
        `).join("")}
      </section>
    </main>
  `;

  const carousel = document.querySelector<HTMLElement>(".carousel");
  if (carousel) {
    enableDragging(carousel);
    document.addEventListener("wheel", (event) => {
      if (event.deltaX === 0 && event.deltaY === 0) return;
      event.preventDefault();
      carousel.scrollLeft += event.deltaX || event.deltaY;
    }, { passive: false });
  }

  document.querySelectorAll<HTMLButtonElement>(".shoe").forEach((button) => {
    button.addEventListener("click", () => {
      const selectedShoe = shoes.find((shoe) => shoe.id === button.dataset.shoeId);
      if (!selectedShoe) return;
      document.body.insertAdjacentHTML("beforeend", renderDetail(selectedShoe));
      const detail = document.querySelector<HTMLElement>(".detail");
      detail?.querySelector(".close-button")?.addEventListener("click", () => detail.remove());
      detail?.addEventListener("click", (event) => {
        if (event.target === detail) detail.remove();
      });
    });
  });
};

const loadShoes = async (): Promise<void> => {
  const response = await fetch("/api/shoes");
  if (!response.ok) throw new Error(`Could not load shoes (${response.status}).`);
  render(await response.json() as Shoe[]);
};

loadShoes().catch((error: unknown) => {
  app.innerHTML = `<p class="error">Unable to load the collection. ${error instanceof Error ? error.message : "Try again later."}</p>`;
});
