(function () {
  const btn = document.querySelector(".menu-btn");
  const sidebar = document.querySelector(".sidebar");
  if (btn && sidebar) {
    btn.addEventListener("click", () => sidebar.classList.toggle("open"));
    document.querySelector(".main")?.addEventListener("click", () => {
      sidebar.classList.remove("open");
    });
  }

  const here = location.pathname.replace(/\/+$/, "").split("/").pop() || "index.html";
  document.querySelectorAll(".nav a[href]").forEach((a) => {
    const href = a.getAttribute("href").split("#")[0];
    if (href === here || (here === "" && href === "index.html")) {
      a.classList.add("active");
    }
  });

  const lang = document.documentElement.lang || "es";
  const INDEX_ES = [
    { page: "index.html", title: "Portada e inicio rápido", text: "kk-5s sierra volante corte en frio aogang kaikong encendido origen ejes" },
    { page: "safety.html", title: "Precauciones de seguridad", text: "electrico gabinete puesta a tierra partes moviles paro de emergencia" },
    { page: "parameters.html#screen-overview", title: "1.1 Vista de pantallas", text: "pantalla tactil navegacion estado produccion parametros idioma" },
    { page: "parameters.html#main-page", title: "1.2.1 Pantalla principal", text: "velocidad de linea longitud de corte posicion carro cantidad" },
    { page: "parameters.html#length", title: "1.2.2 Programación de longitudes", text: "ordenes cantidad produccion ilimitada programa" },
    { page: "parameters.html#tube", title: "1.2.3 Parámetros de tubo", text: "avance espesor diente sierra diametro tiempo de corte" },
    { page: "parameters.html#system", title: "1.2.4 Parámetros de sistema", text: "aceleracion jerk retardo amarre holgura baja velocidad" },
    { page: "parameters.html#manual-params", title: "1.2.5 Parámetros manuales", text: "jog origen lubricacion hidraulico par torque" },
    { page: "parameters.html#motor", title: "1.2.6 Parámetros de motor", text: "velocidad nominal diametro engranaje reduccion husillo variador" },
    { page: "parameters.html#manual-op", title: "1.2.7 Operación manual", text: "botones arrastre avance corte amarre" },
    { page: "functions.html#modes", title: "2.1 Modos de operación", text: "manual simulacion automatico selector" },
    { page: "functions.html#power", title: "2.2 Gestión de energía", text: "breaker servo enable proteccion apagado 20 segundos" },
    { page: "functions.html#jog", title: "2.3 Jog", text: "desplazamiento manual limites" },
    { page: "functions.html#home", title: "2.4 Retorno al origen", text: "origen arrastre origen avance par" },
    { page: "functions.html#clamp-cut", title: "2.5–2.6 Amarre y corte", text: "amarre manual corte estatico utillaje" },
    { page: "functions.html#short-long", title: "2.7 Pieza corta y larga", text: "chatarra costura soldadura" },
    { page: "functions.html#memory", title: "2.7 Memoria de longitud", text: "apagado reanudar produccion punto de memoria" },
    { page: "functions.html#scheduling", title: "2.8 Programación de órdenes", text: "10 programas recetas" },
    { page: "operation.html#power-on", title: "3.1 Encendido", text: "inicializacion 60 segundos unidad hidraulica" },
    { page: "operation.html#jog", title: "3.2 Avance manual", text: "adelante atras jog" },
    { page: "operation.html#home", title: "3.3 Procedimiento de origen", text: "origen arrastre origen avance reset" },
    { page: "operation.html#torque", title: "3.4 Prueba de par de avance", text: "lubricacion 1-15 por ciento" },
    { page: "operation.html#clamp", title: "3.5 Amarre manual", text: "neumatico hidraulico holgura" },
    { page: "operation.html#cut", title: "3.6 Corte manual", text: "corte estatico formadora no debe moverse hoja" },
    { page: "operation.html#sim", title: "3.7 Simulación", text: "eje virtual sin material vuelco carro" },
    { page: "operation.html#auto", title: "3.8 Modo automático", text: "encoder corte a longitud fija" },
    { page: "operation.html#schedule", title: "3.9 Programas de producción", text: "calcular siguiente orden cantidad" },
    { page: "operation.html#memory", title: "3.10 Puntos de memoria", text: "continuar reiniciar origen" },
    { page: "operation.html#short-long", title: "3.11 Piezas cortas y largas", text: "60 por ciento velocidad maxima" },
    { page: "operation.html#sync", title: "3.12 Medición de sincronismo", text: "diametro rueda encoder longitud real espesor hoja" }
  ];
  const INDEX_EN = [
    { page: "index.html", title: "Cover & quick start", text: "kk-5s cold-cut flying saw aogang kaikong power on home axes" },
    { page: "safety.html", title: "Safety precautions", text: "electrical cabinet grounding moving parts non-professionals emergency stop" },
    { page: "parameters.html#screen-overview", title: "1.1 Screen overview", text: "touchscreen navigation production status system settings language" },
    { page: "parameters.html#main-page", title: "1.2.1 Main page", text: "line speed cut length saw car position quantity produced" },
    { page: "parameters.html#length", title: "1.2.2 Length scheduling", text: "orders quantity unlimited production schedule" },
    { page: "parameters.html#tube", title: "1.2.3 Tube type parameters", text: "feed distance wall thickness stfl saw blade teeth diameter cutting time" },
    { page: "parameters.html#system", title: "1.2.4 System parameters", text: "acceleration jerk clamping delay return delay slow-speed allowance" },
    { page: "parameters.html#manual-params", title: "1.2.5 Manual parameters", text: "jog speed home lubrication hydraulic torque limit" },
    { page: "parameters.html#motor", title: "1.2.6 Motor parameters", text: "rated speed gear diameter reduction ratio screw pitch inverter" },
    { page: "parameters.html#manual-op", title: "1.2.7 Manual operation screen", text: "manual buttons drive feed cutting clamp" },
    { page: "functions.html#modes", title: "2.1 Operating modes", text: "manual simulation automatic selector knob" },
    { page: "functions.html#power", title: "2.2 Power management", text: "circuit breaker servo enable power-off protection 20 seconds" },
    { page: "functions.html#jog", title: "2.3 Jog", text: "drag jog feed jog limit switch" },
    { page: "functions.html#home", title: "2.4 Homing", text: "drag-to-home feed home manual home torque" },
    { page: "functions.html#clamp-cut", title: "2.5–2.6 Clamp and cut", text: "manual clamp static cut fixture" },
    { page: "functions.html#short-long", title: "2.7 Short and long length", text: "defective weld point skip cut" },
    { page: "functions.html#memory", title: "2.7 Length memory", text: "power outage resume production memory point" },
    { page: "functions.html#scheduling", title: "2.8 Order scheduling", text: "10 length schedules recipes" },
    { page: "operation.html#power-on", title: "3.1 Power-on", text: "initialization 60 seconds hydraulic unit" },
    { page: "operation.html#jog", title: "3.2 Manual feed", text: "forward reverse jog knob" },
    { page: "operation.html#home", title: "3.3 Homing procedure", text: "drive home feed home reset" },
    { page: "operation.html#torque", title: "3.4 Feed torque test", text: "lubrication 1-15 percent machine learning" },
    { page: "operation.html#clamp", title: "3.5 Manual clamping", text: "pneumatic hydraulic wobble gap" },
    { page: "operation.html#cut", title: "3.6 Manual cutting", text: "static cut forming unit must not move blade damage" },
    { page: "operation.html#sim", title: "3.7 Simulation", text: "virtual axis no material saw carriage overturning" },
    { page: "operation.html#auto", title: "3.8 Automatic mode", text: "encoder online fixed-length cutting" },
    { page: "operation.html#schedule", title: "3.9 Production schedules", text: "calculate next order reset quantity" },
    { page: "operation.html#memory", title: "3.10 Memory points", text: "continue restart home" },
    { page: "operation.html#short-long", title: "3.11 Short and long pieces", text: "60 percent max line speed" },
    { page: "operation.html#sync", title: "3.12 Synchronization measurement", text: "encoder wheel diameter actual material length blade thickness" }
  ];

  const INDEX = lang.startsWith("es") ? INDEX_ES : INDEX_EN;
  const emptyMsg = lang.startsWith("es") ? "No hay secciones coincidentes." : "No matching sections.";

  const input = document.querySelector("#manual-search");
  const box = document.querySelector("#search-results");
  if (!input || !box) return;

  function render(q) {
    const term = q.trim().toLowerCase();
    if (term.length < 2) {
      box.style.display = "none";
      box.innerHTML = "";
      return;
    }
    const hits = INDEX.filter((item) =>
      (item.title + " " + item.text).toLowerCase().includes(term)
    ).slice(0, 12);
    if (!hits.length) {
      box.style.display = "block";
      box.innerHTML = `<div style='padding:10px 12px;font-size:13px;color:#5a6a7a'>${emptyMsg}</div>`;
      return;
    }
    box.style.display = "block";
    box.innerHTML = hits
      .map(
        (h) =>
          `<a href="${h.page}"><span class="page">${h.page.replace(".html", "")}</span><br>${h.title}</a>`
      )
      .join("");
  }

  input.addEventListener("input", (e) => render(e.target.value));
  input.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      box.style.display = "none";
      input.blur();
    }
  });
  document.addEventListener("click", (e) => {
    if (!e.target.closest(".search-wrap")) box.style.display = "none";
  });
})();
