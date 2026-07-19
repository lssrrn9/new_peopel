/**
 * Plantilla de curso — lógica sencilla
 *
 * Idea para un niño de 10 años:
 * En el HTML hay una cajita mágica llamada data-course-title.
 * Este script lee esa cajita y copia el título en todos los
 * sitios de la página que llevan la clase .js-course-title.
 * Así solo cambias el título UNA vez.
 */

(function () {
  "use strict";

  const root = document.getElementById("curso");
  if (!root) return;

  const title = (root.dataset.courseTitle || "").trim();
  const tagline = (root.dataset.courseTagline || "").trim();

  if (title) {
    document.title = title;
    document.querySelectorAll(".js-course-title").forEach(function (el) {
      el.textContent = title;
    });
  }

  if (tagline) {
    document.querySelectorAll(".js-course-tagline").forEach(function (el) {
      el.textContent = tagline;
    });
  }

  // Menú móvil
  const toggle = document.querySelector(".nav-toggle");
  const menu = document.getElementById("menu-movil");

  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      const open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      toggle.setAttribute("aria-label", open ? "Abrir menú" : "Cerrar menú");
      menu.hidden = open;
    });

    menu.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        toggle.setAttribute("aria-expanded", "false");
        toggle.setAttribute("aria-label", "Abrir menú");
        menu.hidden = true;
      });
    });
  }

  // Aparición suave de módulos al hacer scroll
  const modules = document.querySelectorAll(".module");
  if ("IntersectionObserver" in window && modules.length) {
    const observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.2, rootMargin: "0px 0px -40px 0px" }
    );

    modules.forEach(function (mod, i) {
      mod.style.transitionDelay = i * 80 + "ms";
      observer.observe(mod);
    });
  } else {
    modules.forEach(function (mod) {
      mod.classList.add("is-visible");
    });
  }
})();
