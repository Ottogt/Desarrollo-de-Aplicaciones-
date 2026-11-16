const STORAGE_KEY = "seguritoapp_v1";

const AFFILIATES = {
  medicos: [
    { id: "m1", nombre: "Dra. Ana Lucía Méndez", especialidad: "Medicina interna", zona: "Zona 10", telefono: "2222-1101", horario: "Lun–Vie 8:00–16:00" },
    { id: "m2", nombre: "Dr. Carlos Rivera", especialidad: "Cardiología", zona: "Zona 15", telefono: "2222-1102", horario: "Mar–Sáb 9:00–17:00" },
    { id: "m3", nombre: "Dra. Sofía Castillo", especialidad: "Pediatría", zona: "Zona 9", telefono: "2222-1103", horario: "Lun–Vie 7:30–15:30" },
    { id: "m4", nombre: "Dr. Luis Paredes", especialidad: "Traumatología", zona: "Zona 11", telefono: "2222-1104", horario: "Lun–Vie 10:00–18:00" },
  ],
  hospitales: [
    { id: "h1", nombre: "Hospital El Roble", especialidad: "Hospital general", zona: "Zona 10", telefono: "2333-2201", horario: "24 horas" },
    { id: "h2", nombre: "Clínica La Ceiba", especialidad: "Cirugía y emergencia", zona: "Zona 14", telefono: "2333-2202", horario: "24 horas" },
    { id: "h3", nombre: "Centro Médico Ciprés", especialidad: "Hospitalización corta", zona: "Zona 15", telefono: "2333-2203", horario: "24 horas" },
  ],
  laboratorios: [
    { id: "l1", nombre: "Lab Árbol Verde", especialidad: "Clínico completo", zona: "Zona 9", telefono: "2444-3301", horario: "Lun–Sáb 6:00–18:00" },
    { id: "l2", nombre: "Diagnósticos Pino", especialidad: "Imagen y laboratorio", zona: "Zona 10", telefono: "2444-3302", horario: "Lun–Vie 7:00–19:00" },
    { id: "l3", nombre: "BioLab Encino", especialidad: "Especializado", zona: "Zona 4", telefono: "2444-3303", horario: "Lun–Vie 6:30–17:30" },
  ],
};

const DEFAULT_STATE = {
  user: null,
  solicitudes: [
    {
      id: "SOL-1001",
      tipo: "medicamento",
      titulo: "Losartán 50 mg",
      detalle: "Tratamiento hipertensión · 30 tabletas",
      fecha: "2026-11-05",
      estado: "aprobada",
      medico: "Dra. Ana Lucía Méndez",
      notas: "Autorizado por 30 días.",
    },
    {
      id: "SOL-1002",
      tipo: "hospitalizacion",
      titulo: "Hospitalización programada",
      detalle: "Hospital El Roble · 2 noches",
      fecha: "2026-11-07",
      estado: "en_revision",
      medico: "Dr. Carlos Rivera",
      notas: "Pendiente de validación médica.",
    },
    {
      id: "SOL-1003",
      tipo: "medicamento",
      titulo: "Amoxicilina 500 mg",
      detalle: "Infección respiratoria · 21 cápsulas",
      fecha: "2026-11-01",
      estado: "rechazada",
      medico: "Dra. Sofía Castillo",
      notas: "El medicamento no está en el cuadro básico de la póliza.",
    },
  ],
  notificaciones: [
    {
      id: "n1",
      titulo: "Autorización aprobada",
      cuerpo: "SOL-1001 · Losartán 50 mg fue aprobada.",
      fecha: "2026-11-06 09:20",
      tipo: "aprobada",
      leida: false,
      solicitudId: "SOL-1001",
    },
    {
      id: "n2",
      titulo: "Autorización en revisión",
      cuerpo: "SOL-1002 · Hospitalización recibida y en análisis.",
      fecha: "2026-11-07 14:05",
      tipo: "en_revision",
      leida: false,
      solicitudId: "SOL-1002",
    },
    {
      id: "n3",
      titulo: "Autorización rechazada",
      cuerpo: "SOL-1003 · Amoxicilina 500 mg fue rechazada.",
      fecha: "2026-11-02 11:40",
      tipo: "rechazada",
      leida: true,
      solicitudId: "SOL-1003",
    },
  ],
};

function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return structuredClone(DEFAULT_STATE);
    return { ...structuredClone(DEFAULT_STATE), ...JSON.parse(raw) };
  } catch {
    return structuredClone(DEFAULT_STATE);
  }
}

function saveState() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

let state = loadState();
let route = state.user ? { name: "home" } : { name: "login" };
let toastTimer = null;

const app = document.getElementById("app");

function navigate(name, params = {}) {
  route = { name, params };
  render();
}

function showToast(message) {
  const existing = document.querySelector(".toast");
  if (existing) existing.remove();
  const el = document.createElement("div");
  el.className = "toast";
  el.textContent = message;
  app.appendChild(el);
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => el.remove(), 2400);
}

function statusBar() {
  return `<div class="status-bar"><span>9:41</span><span>LTE · 80%</span></div>`;
}

function bottomNav(active) {
  const unread = state.notificaciones.filter((n) => !n.leida).length;
  const items = [
    { id: "home", label: "Inicio", icon: "⌂" },
    { id: "afiliados", label: "Afiliados", icon: "✚" },
    { id: "solicitudes", label: "Solicitudes", icon: "☰" },
    { id: "notificaciones", label: "Avisos", icon: unread ? `•${unread}` : "⚑" },
  ];
  return `<nav class="bottom-nav">${items
    .map(
      (i) => `<button class="nav-item ${active === i.id ? "active" : ""}" data-nav="${i.id}">
        <span class="ni">${i.icon}</span>${i.label}
      </button>`
    )
    .join("")}</nav>`;
}

function badge(estado) {
  const map = {
    aprobada: ["badge-ok", "Aprobada"],
    rechazada: ["badge-danger", "Rechazada"],
    en_revision: ["badge-warn", "En revisión"],
  };
  const [cls, label] = map[estado] || ["badge-info", estado];
  return `<span class="badge ${cls}">${label}</span>`;
}

function topbar(title, { back, right } = {}) {
  return `<div class="topbar">
    ${back ? `<button class="back-btn" data-back="${back}">←</button>` : `<span style="width:36px"></span>`}
    <h2>${title}</h2>
    ${right || `<span style="width:36px"></span>`}
  </div>`;
}

function renderLogin() {
  app.innerHTML = `
    <section class="app-screen">
      <div class="hero-login">
        <div class="brand-mark">🌳</div>
        <h1>SeguritoApp</h1>
        <p>Tu red afiliada y autorizaciones médicas con El Gran Árbol.</p>
        <div class="login-card">
          <h2>Iniciar sesión</h2>
          <p class="sub">Ingresa tus credenciales para continuar</p>
          <div id="login-error" hidden class="error"></div>
          <label class="label" for="email">Correo</label>
          <input class="field" id="email" type="email" placeholder="correo@ejemplo.com" autocomplete="username" />
          <label class="label" for="password">Contraseña</label>
          <input class="field" id="password" type="password" placeholder="••••••••" autocomplete="current-password" />
          <button class="btn btn-primary" id="btn-login">Ingresar</button>
        </div>
      </div>
    </section>`;

  document.getElementById("btn-login").onclick = () => {
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const err = document.getElementById("login-error");
    if (!email || !password) {
      err.hidden = false;
      err.textContent = "Completa correo y contraseña para continuar.";
      return;
    }
    state.user = {
      nombre: "Otto Hernandez",
      email,
      poliza: "GA-08001620",
      plan: "Familiar Plus",
    };
    saveState();
    navigate("home");
    showToast("Bienvenido a SeguritoApp");
  };
}

function renderHome() {
  const pendientes = state.solicitudes.filter((s) => s.estado === "en_revision").length;
  const unread = state.notificaciones.filter((n) => !n.leida).length;
  app.innerHTML = `
    <section class="app-screen">
      ${statusBar()}
      ${topbar("SeguritoApp", {
        right: `<button class="icon-btn" data-nav="perfil" title="Perfil">👤</button>`,
      })}
      <div class="content">
        <div class="home-hero">
          <p class="hello">Hola, ${state.user.nombre.split(" ")[0]}</p>
          <h3>El Gran Árbol cuida tu salud</h3>
          <div class="policy">Póliza ${state.user.poliza} · ${state.user.plan}</div>
        </div>
        <div class="grid-2">
          <button class="tile" data-go="afiliados" data-tipo="medicos"><span class="glyph">🩺</span><strong>Médicos</strong><span>Red afiliada</span></button>
          <button class="tile" data-go="afiliados" data-tipo="hospitales"><span class="glyph">🏥</span><strong>Hospitales</strong><span>Centros de atención</span></button>
          <button class="tile" data-go="afiliados" data-tipo="laboratorios"><span class="glyph">🧪</span><strong>Laboratorios</strong><span>Estudios clínicos</span></button>
          <button class="tile" data-go="nueva"><span class="glyph">📝</span><strong>Nueva solicitud</strong><span>Medicamento u hosp.</span></button>
        </div>
        <p class="section-title">Resumen</p>
        <div class="grid-2">
          <div class="stat"><strong>${pendientes}</strong><div class="muted">En revisión</div></div>
          <div class="stat"><strong>${unread}</strong><div class="muted">Avisos nuevos</div></div>
        </div>
        <p class="section-title">Accesos rápidos</p>
        <button class="btn btn-secondary" data-nav="solicitudes">Ver registro de autorizaciones</button>
        <button class="btn btn-ghost" data-nav="notificaciones" style="margin-top:10px">Abrir notificaciones</button>
      </div>
      ${bottomNav("home")}
    </section>`;
  bindNav();
  document.querySelectorAll("[data-go]").forEach((el) => {
    el.onclick = () => {
      if (el.dataset.go === "nueva") navigate("nueva");
      else navigate("afiliados", { tipo: el.dataset.tipo || "medicos" });
    };
  });
}

function renderAfiliados() {
  const tipo = route.params.tipo || "medicos";
  const q = (route.params.q || "").toLowerCase();
  const labels = { medicos: "Médicos", hospitales: "Hospitales", laboratorios: "Laboratorios" };
  const list = AFFILIATES[tipo].filter((item) => {
    const hay = `${item.nombre} ${item.especialidad} ${item.zona}`.toLowerCase();
    return hay.includes(q);
  });

  app.innerHTML = `
    <section class="app-screen">
      ${statusBar()}
      ${topbar("Afiliados")}
      <div class="content">
        <div class="chips">
          ${Object.keys(labels)
            .map(
              (key) =>
                `<button class="chip ${tipo === key ? "active" : ""}" data-tipo="${key}">${labels[key]}</button>`
            )
            .join("")}
        </div>
        <div class="search">
          <input id="search" placeholder="Buscar por nombre, especialidad o zona" value="${route.params.q || ""}" />
        </div>
        ${
          list.length
            ? list
                .map(
                  (item) => `<button class="list-card" data-id="${item.id}" data-tipo="${tipo}">
                    <div class="avatar">${item.nombre.split(" ").slice(0, 2).map((p) => p[0]).join("")}</div>
                    <div>
                      <h4>${item.nombre}</h4>
                      <p>${item.especialidad}<br>${item.zona} · ${item.horario}</p>
                    </div>
                    <span>›</span>
                  </button>`
                )
                .join("")
            : `<div class="empty"><strong>Sin resultados</strong><div class="muted">Prueba con otro término o categoría.</div></div>`
        }
      </div>
      ${bottomNav("afiliados")}
    </section>`;

  bindNav();
  document.querySelectorAll("[data-tipo]").forEach((chip) => {
    if (!chip.classList.contains("chip")) return;
    chip.onclick = () => navigate("afiliados", { tipo: chip.dataset.tipo, q: document.getElementById("search").value });
  });
  const search = document.getElementById("search");
  search.oninput = () => {
    clearTimeout(search._t);
    search._t = setTimeout(() => navigate("afiliados", { tipo, q: search.value }), 180);
  };
  document.querySelectorAll(".list-card").forEach((card) => {
    card.onclick = () => navigate("detalle-afiliado", { tipo: card.dataset.tipo, id: card.dataset.id });
  });
}

function renderDetalleAfiliado() {
  const item = AFFILIATES[route.params.tipo].find((x) => x.id === route.params.id);
  if (!item) return navigate("afiliados");
  app.innerHTML = `
    <section class="app-screen">
      ${statusBar()}
      ${topbar("Detalle", { back: "afiliados" })}
      <div class="content">
        <div class="detail-card">
          <div class="avatar" style="width:64px;height:64px;border-radius:20px;font-size:20px;margin-bottom:12px">${item.nombre
            .split(" ")
            .slice(0, 2)
            .map((p) => p[0])
            .join("")}</div>
          <h3>${item.nombre}</h3>
          <p class="muted">${item.especialidad}</p>
          <div class="kv">
            <div><span>Zona</span><strong>${item.zona}</strong></div>
            <div><span>Teléfono</span><strong>${item.telefono}</strong></div>
            <div><span>Horario</span><strong>${item.horario}</strong></div>
            <div><span>Estado</span><strong>Afiliado activo</strong></div>
          </div>
          <button class="btn btn-primary" id="btn-solicitar">Solicitar autorización</button>
        </div>
      </div>
      ${bottomNav("afiliados")}
    </section>`;
  bindNav();
  document.querySelector("[data-back]").onclick = () => navigate("afiliados", { tipo: route.params.tipo });
  document.getElementById("btn-solicitar").onclick = () =>
    navigate("nueva", {
      tipo: route.params.tipo === "hospitales" ? "hospitalizacion" : "medicamento",
      pref: item.nombre,
    });
}

function renderNueva() {
  const tipo = route.params.tipo || "medicamento";
  app.innerHTML = `
    <section class="app-screen">
      ${statusBar()}
      ${topbar("Nueva solicitud", { back: "home" })}
      <div class="content">
        <div class="tabs">
          <button class="tab ${tipo === "medicamento" ? "active" : ""}" data-tipo="medicamento">Medicamento</button>
          <button class="tab ${tipo === "hospitalizacion" ? "active" : ""}" data-tipo="hospitalizacion">Hospitalización</button>
        </div>
        <div class="form-card">
          <h3>${tipo === "medicamento" ? "Autorización de medicamento" : "Autorización de hospitalización"}</h3>
          <p class="muted">Completa los datos. Quedará registrada y recibirás notificación de aprobación o rechazo.</p>
          <label class="label" for="titulo">${tipo === "medicamento" ? "Medicamento" : "Motivo / procedimiento"}</label>
          <input class="field" id="titulo" placeholder="${tipo === "medicamento" ? "Ej. Metformina 850 mg" : "Ej. Cirugía programada rodilla"}" />
          <label class="label" for="detalle">Detalle</label>
          <input class="field" id="detalle" placeholder="${tipo === "medicamento" ? "Dosis, cantidad y duración" : "Hospital, días estimados"}" value="${route.params.pref || ""}" />
          <label class="label" for="medico">Médico tratante</label>
          <select class="field" id="medico">
            ${AFFILIATES.medicos.map((m) => `<option>${m.nombre}</option>`).join("")}
          </select>
          <p class="helper">La solicitud queda en estado “En revisión” hasta la respuesta de la aseguradora.</p>
          <button class="btn btn-primary" id="btn-enviar">Enviar solicitud</button>
        </div>
      </div>
      ${bottomNav("solicitudes")}
    </section>`;
  bindNav();
  document.querySelector("[data-back]").onclick = () => navigate("home");
  document.querySelectorAll(".tab").forEach((tab) => {
    tab.onclick = () => navigate("nueva", { tipo: tab.dataset.tipo, pref: route.params.pref });
  });
  document.getElementById("btn-enviar").onclick = () => {
    const titulo = document.getElementById("titulo").value.trim();
    const detalle = document.getElementById("detalle").value.trim();
    const medico = document.getElementById("medico").value;
    if (!titulo || !detalle) {
      showToast("Completa los campos obligatorios");
      return;
    }
    const id = `SOL-${1000 + state.solicitudes.length + 1}`;
    const hoy = new Date();
    const fecha = hoy.toISOString().slice(0, 10);
    const hora = hoy.toLocaleString("es-GT", { hour: "2-digit", minute: "2-digit" });
    state.solicitudes.unshift({
      id,
      tipo,
      titulo,
      detalle,
      fecha,
      estado: "en_revision",
      medico,
      notas: "Solicitud recibida. Pendiente de análisis.",
    });
    state.notificaciones.unshift({
      id: `n${Date.now()}`,
      titulo: "Solicitud enviada",
      cuerpo: `${id} · ${titulo} está en revisión.`,
      fecha: `${fecha} ${hora}`,
      tipo: "en_revision",
      leida: false,
      solicitudId: id,
    });
    // Simulación de respuesta automática para el prototipo
    setTimeout(() => resolverSolicitud(id), 3500);
    saveState();
    navigate("detalle-solicitud", { id });
    showToast("Solicitud registrada");
  };
}

function resolverSolicitud(id) {
  const sol = state.solicitudes.find((s) => s.id === id);
  if (!sol || sol.estado !== "en_revision") return;
  const aprobar = !/experimental|no cubierto/i.test(`${sol.titulo} ${sol.detalle}`);
  sol.estado = aprobar ? "aprobada" : "rechazada";
  sol.notas = aprobar
    ? "Autorización aprobada. Presenta este folio en la red afiliada."
    : "Autorización rechazada. Verifica cobertura de tu póliza o contacta a tu asesor.";
  const ahora = new Date();
  state.notificaciones.unshift({
    id: `n${Date.now()}`,
    titulo: aprobar ? "Autorización aprobada" : "Autorización rechazada",
    cuerpo: `${sol.id} · ${sol.titulo} fue ${aprobar ? "aprobada" : "rechazada"}.`,
    fecha: `${ahora.toISOString().slice(0, 10)} ${ahora.toLocaleString("es-GT", { hour: "2-digit", minute: "2-digit" })}`,
    tipo: sol.estado,
    leida: false,
    solicitudId: sol.id,
  });
  saveState();
  if (["solicitudes", "detalle-solicitud", "notificaciones", "home"].includes(route.name)) render();
}

function renderSolicitudes() {
  const filtro = route.params.filtro || "todas";
  const items = state.solicitudes.filter((s) => (filtro === "todas" ? true : s.estado === filtro));
  app.innerHTML = `
    <section class="app-screen">
      ${statusBar()}
      ${topbar("Solicitudes", {
        right: `<button class="icon-btn" data-nav="nueva">＋</button>`,
      })}
      <div class="content">
        <div class="chips">
          ${[
            ["todas", "Todas"],
            ["en_revision", "En revisión"],
            ["aprobada", "Aprobadas"],
            ["rechazada", "Rechazadas"],
          ]
            .map(
              ([id, label]) =>
                `<button class="chip ${filtro === id ? "active" : ""}" data-filtro="${id}">${label}</button>`
            )
            .join("")}
        </div>
        ${
          items.length
            ? items
                .map(
                  (s) => `<button class="list-card" data-id="${s.id}">
                    <div class="avatar">${s.tipo === "medicamento" ? "💊" : "🛏️"}</div>
                    <div>
                      <h4>${s.titulo}</h4>
                      <p>${s.id} · ${s.fecha}<br>${s.detalle}</p>
                    </div>
                    ${badge(s.estado)}
                  </button>`
                )
                .join("")
            : `<div class="empty"><strong>No hay solicitudes</strong><div class="muted">Crea una nueva autorización de medicamento u hospitalización.</div>
                <button class="btn btn-primary" style="margin-top:14px" data-nav="nueva">Nueva solicitud</button></div>`
        }
      </div>
      ${bottomNav("solicitudes")}
    </section>`;
  bindNav();
  document.querySelectorAll("[data-filtro]").forEach((chip) => {
    chip.onclick = () => navigate("solicitudes", { filtro: chip.dataset.filtro });
  });
  document.querySelectorAll(".list-card").forEach((card) => {
    card.onclick = () => navigate("detalle-solicitud", { id: card.dataset.id });
  });
}

function renderDetalleSolicitud() {
  const s = state.solicitudes.find((x) => x.id === route.params.id);
  if (!s) return navigate("solicitudes");
  app.innerHTML = `
    <section class="app-screen">
      ${statusBar()}
      ${topbar("Detalle", { back: "solicitudes" })}
      <div class="content">
        <div class="detail-card">
          <div style="display:flex;justify-content:space-between;gap:12px;align-items:center">
            <h3>${s.titulo}</h3>
            ${badge(s.estado)}
          </div>
          <p class="muted">${s.tipo === "medicamento" ? "Medicamento" : "Hospitalización"} · ${s.id}</p>
          <div class="kv">
            <div><span>Fecha</span><strong>${s.fecha}</strong></div>
            <div><span>Médico</span><strong>${s.medico}</strong></div>
            <div><span>Detalle</span><strong>${s.detalle}</strong></div>
          </div>
          <p class="section-title" style="margin-top:4px">Seguimiento</p>
          <div class="timeline">
            <div class="timeline-item"><strong>Solicitud enviada</strong><span>${s.fecha}</span></div>
            <div class="timeline-item"><strong>${s.estado === "en_revision" ? "En revisión" : s.estado === "aprobada" ? "Aprobada" : "Rechazada"}</strong><span>${s.notas}</span></div>
          </div>
        </div>
      </div>
      ${bottomNav("solicitudes")}
    </section>`;
  bindNav();
  document.querySelector("[data-back]").onclick = () => navigate("solicitudes");
}

function renderNotificaciones() {
  app.innerHTML = `
    <section class="app-screen">
      ${statusBar()}
      ${topbar("Notificaciones", {
        right: `<button class="icon-btn" id="mark-all" title="Marcar leídas">✓</button>`,
      })}
      <div class="content">
        ${
          state.notificaciones.length
            ? state.notificaciones
                .map((n) => {
                  const color =
                    n.tipo === "aprobada"
                      ? "var(--ok-soft)"
                      : n.tipo === "rechazada"
                        ? "var(--danger-soft)"
                        : "var(--warn-soft)";
                  const icon = n.tipo === "aprobada" ? "✓" : n.tipo === "rechazada" ? "!" : "…";
                  return `<button class="notif ${n.leida ? "" : "unread"}" data-id="${n.id}" data-sol="${n.solicitudId || ""}">
                    <div class="dot" style="background:${color}">${icon}</div>
                    <div>
                      <h4>${n.titulo}</h4>
                      <p>${n.cuerpo}<br>${n.fecha}</p>
                    </div>
                  </button>`;
                })
                .join("")
            : `<div class="empty"><strong>Sin notificaciones</strong><div class="muted">Aquí verás aprobaciones y rechazos.</div></div>`
        }
      </div>
      ${bottomNav("notificaciones")}
    </section>`;
  bindNav();
  document.getElementById("mark-all").onclick = () => {
    state.notificaciones.forEach((n) => (n.leida = true));
    saveState();
    render();
    showToast("Notificaciones marcadas como leídas");
  };
  document.querySelectorAll(".notif").forEach((el) => {
    el.onclick = () => {
      const n = state.notificaciones.find((x) => x.id === el.dataset.id);
      if (n) n.leida = true;
      saveState();
      if (el.dataset.sol) navigate("detalle-solicitud", { id: el.dataset.sol });
      else render();
    };
  });
}

function renderPerfil() {
  app.innerHTML = `
    <section class="app-screen">
      ${statusBar()}
      ${topbar("Mi cuenta", { back: "home" })}
      <div class="content">
        <div class="detail-card">
          <h3>${state.user.nombre}</h3>
          <p class="muted">${state.user.email}</p>
          <div class="kv">
            <div><span>Póliza</span><strong>${state.user.poliza}</strong></div>
            <div><span>Plan</span><strong>${state.user.plan}</strong></div>
            <div><span>Aseguradora</span><strong>El Gran Árbol</strong></div>
          </div>
          <button class="btn btn-danger" id="logout">Cerrar sesión</button>
        </div>
      </div>
      ${bottomNav("home")}
    </section>`;
  bindNav();
  document.querySelector("[data-back]").onclick = () => navigate("home");
  document.getElementById("logout").onclick = () => {
    state.user = null;
    saveState();
    navigate("login");
  };
}

function bindNav() {
  document.querySelectorAll("[data-nav]").forEach((el) => {
    el.onclick = () => navigate(el.dataset.nav);
  });
}

function render() {
  const map = {
    login: renderLogin,
    home: renderHome,
    afiliados: renderAfiliados,
    "detalle-afiliado": renderDetalleAfiliado,
    nueva: renderNueva,
    solicitudes: renderSolicitudes,
    "detalle-solicitud": renderDetalleSolicitud,
    notificaciones: renderNotificaciones,
    perfil: renderPerfil,
  };
  (map[route.name] || renderHome)();
}

render();
