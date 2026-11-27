/* ===== Animatrixx Developer — interactions ===== */

(function () {
  "use strict";

  var WHATSAPP = "2347045257764"; // digits only, country code included

  /* ---------- Mobile navigation ---------- */
  var toggle = document.getElementById("navToggle");
  var nav = document.getElementById("siteNav");

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      nav.classList.toggle("is-open", !open);
    });

    nav.addEventListener("click", function (event) {
      if (event.target.closest("a")) {
        toggle.setAttribute("aria-expanded", "false");
        nav.classList.remove("is-open");
      }
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && nav.classList.contains("is-open")) {
        toggle.setAttribute("aria-expanded", "false");
        nav.classList.remove("is-open");
        toggle.focus();
      }
    });
  }

  /* ---------- Scroll reveal ---------- */
  var revealItems = document.querySelectorAll(".reveal");

  if (revealItems.length) {
    var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    if (reduced || !("IntersectionObserver" in window)) {
      revealItems.forEach(function (el) { el.classList.add("is-visible"); });
    } else {
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });

      revealItems.forEach(function (el) { observer.observe(el); });
    }
  }

  /* ---------- Active nav link ---------- */
  var navLinks = Array.prototype.slice.call(document.querySelectorAll('.site-nav a[href^="#"]'));
  var sections = navLinks
    .map(function (link) { return document.querySelector(link.getAttribute("href")); })
    .filter(Boolean);

  if (sections.length && "IntersectionObserver" in window) {
    var navObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        navLinks.forEach(function (link) {
          link.classList.toggle("is-active", link.getAttribute("href") === "#" + entry.target.id);
        });
      });
    }, { rootMargin: "-45% 0px -50% 0px" });

    sections.forEach(function (section) { navObserver.observe(section); });
  }

  /* ---------- Contact form -> WhatsApp ---------- */
  var form = document.getElementById("contactForm");
  var hint = document.getElementById("formHint");
  var hintDefault = hint ? hint.textContent : "";

  if (form && hint) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();

      var name = form.elements.name.value.trim();
      var business = form.elements.business.value.trim();
      var need = form.elements.need.value;
      var message = form.elements.message.value.trim();

      if (!name || !need || !message) {
        hint.textContent = "Please add your name, what you need, and a short message.";
        hint.classList.add("is-error");
        if (!name) { form.elements.name.focus(); }
        else if (!need) { form.elements.need.focus(); }
        else { form.elements.message.focus(); }
        return;
      }

      hint.textContent = hintDefault;
      hint.classList.remove("is-error");

      var lines = [
        "Hello, I found Animatrixx Developer online.",
        "",
        "Name: " + name
      ];

      if (business) lines.push("Business: " + business);
      lines.push("I need: " + need);
      lines.push("");
      lines.push(message);

      var url = "https://wa.me/" + WHATSAPP + "?text=" + encodeURIComponent(lines.join("\n"));
      window.open(url, "_blank", "noopener");
    });
  }

  /* ---------- Footer year ---------- */
  var year = document.getElementById("year");
  if (year) year.textContent = String(new Date().getFullYear());
})();
