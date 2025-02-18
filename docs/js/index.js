function nextSlide(id) {
  let s = document.querySelector("#" + id + " .slider-inner"),
    i = parseInt(
      document.querySelector("#" + id).getAttribute("data-index") || "0"
    ),
    l = s.children.length;
  (i = (i + 1) % l),
    document.querySelector("#" + id).setAttribute("data-index", i),
    (s.style.transform = "translateX(-" + i * 100 + "%)");
}
function prevSlide(id) {
  let s = document.querySelector("#" + id + " .slider-inner"),
    i = parseInt(
      document.querySelector("#" + id).getAttribute("data-index") || "0"
    ),
    l = s.children.length;
  (i = (i - 1 + l) % l),
    document.querySelector("#" + id).setAttribute("data-index", i),
    (s.style.transform = "translateX(-" + i * 100 + "%)");
}
setInterval(() => {
  nextSlide("slider1");
  nextSlide("slider2");
}, 5000);
const menuBtn = document.getElementById("menu-btn"),
  mobileMenu = document.getElementById("mobile-menu");
menuBtn.addEventListener("click", () => {
  mobileMenu.classList.toggle("hidden"), menuBtn.classList.toggle("open");
});
const openModalElements = document.querySelectorAll(
    ".open-contact,#open-modal"
  ),
  modal = document.getElementById("contact-modal"),
  closeModal = document.getElementById("close-modal");
openModalElements.forEach((e) => {
  e.addEventListener("click", (t) => {
    t.preventDefault();
    modal.style.display = "block";
    document.body.style.overflow = "hidden";
  });
});
closeModal.addEventListener("click", () => {
  modal.style.display = "none";
  document.body.style.overflow = "auto";
});
window.addEventListener("click", (t) => {
  if (t.target === modal) {
    modal.style.display = "none";
    document.body.style.overflow = "auto";
  }
});
document.querySelectorAll(".card").forEach((e) => {
  e.addEventListener("mouseenter", () => {
    let t = 40 * Math.random() - 20,
      n = 40 * Math.random() - 20;
    e.style.transform = `perspective(1000px) rotateX(${t}deg) rotateY(${n}deg) scale(1.05)`;
  });
  e.addEventListener("mouseleave", () => {
    e.style.transform =
      "perspective(1000px) rotateX(0deg) rotateY(0deg) scale(1)";
  });
});
document.querySelectorAll(".huly-btn").forEach((e) => {
  let t = e.querySelector(".huly-btn-bg");
  e.addEventListener("mousemove", (n) => {
    let o = e.getBoundingClientRect(),
      d = n.clientX - o.left,
      a = n.clientY - o.top,
      r = d - o.width / 2,
      c = a - o.height / 2;
    t.style.transform = `translate(${r}px,${c}px)`;
  });
});
document.querySelectorAll(".wave-divider").forEach((e) => {
  let t = e.querySelector(".wave-drop");
  e.addEventListener("mousemove", (n) => {
    let o = e.getBoundingClientRect();
    (t.style.left = n.clientX - o.left + "px"),
      (t.style.opacity = "1"),
      (t.style.transform = "translateY(0)");
  });
  e.addEventListener("mouseleave", (n) => {
    (t.style.transition = "transform 0.5s,opacity 0.5s"),
      (t.style.transform = "translateY(30px)"),
      (t.style.opacity = "0"),
      setTimeout(() => {
        t.style.transition = "";
      }, 500);
  });
});