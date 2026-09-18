const API_BASE = "http://127.0.0.1:8000";
const USUARIOS_URL = `${API_BASE}/usuarios`;
const PLANIFICAR_URL = `${API_BASE}/planificar`;
const CONSULTAS_URL = `${API_BASE}/consultas`;

const form = document.getElementById("travelForm");
const loading = document.getElementById("loading");
const resultCard = document.getElementById("resultCard");
const errorBox = document.getElementById("errorBox");
const recomendacionesList = document.getElementById("recomendacionesList");
const rutaList = document.getElementById("rutaList");
const explicacionText = document.getElementById("explicacionText");
const welcomeState = document.getElementById("welcomeState");

const navButtons = document.querySelectorAll(".nav-btn");
const planificadorView = document.getElementById("planificadorView");
const historialView = document.getElementById("historialView");
const viewTitle = document.getElementById("viewTitle");
const viewSubtitle = document.getElementById("viewSubtitle");

const historyGrid = document.getElementById("historyGrid");
const historyLoading = document.getElementById("historyLoading");
const historyEmpty = document.getElementById("historyEmpty");
const refreshHistoryBtn = document.getElementById("refreshHistoryBtn");

function limpiarTextoLista(texto) {
  if (!texto.trim()) return [];
  return texto
    .split(",")
    .map(item => item.trim())
    .filter(item => item.length > 0);
}

function mostrarError(mensaje) {
  errorBox.textContent = mensaje;
  errorBox.classList.remove("hidden");
}

function ocultarError() {
  errorBox.classList.add("hidden");
  errorBox.textContent = "";
}

function mostrarLoading() {
  loading.classList.remove("hidden");
}

function ocultarLoading() {
  loading.classList.add("hidden");
}

function limpiarResultado() {
  recomendacionesList.innerHTML = "";
  rutaList.innerHTML = "";
  explicacionText.textContent = "";
  resultCard.classList.add("hidden");
  welcomeState.classList.remove("hidden");
}

function mostrarResultado(data) {
  const consulta = data.consulta;

  recomendacionesList.innerHTML = "";
  rutaList.innerHTML = "";

  consulta.recomendaciones.forEach(destino => {
    const li = document.createElement("li");
    li.textContent = destino;
    recomendacionesList.appendChild(li);
  });

  consulta.ruta_sugerida.forEach(destino => {
    const li = document.createElement("li");
    li.textContent = destino;
    rutaList.appendChild(li);
  });

  explicacionText.textContent = consulta.explicacion_ia;
  welcomeState.classList.add("hidden");
  resultCard.classList.remove("hidden");
}

function cambiarVista(viewName) {
  navButtons.forEach(btn => btn.classList.remove("active"));
  document.querySelector(`.nav-btn[data-view="${viewName}"]`).classList.add("active");

  if (viewName === "planificador") {
    planificadorView.classList.add("active-view");
    historialView.classList.remove("active-view");
    viewTitle.textContent = "Planificador de viajes";
    viewSubtitle.textContent = "Ingresa tu perfil y recibe recomendaciones personalizadas";
  } else {
    historialView.classList.add("active-view");
    planificadorView.classList.remove("active-view");
    viewTitle.textContent = "Historial de consultas";
    viewSubtitle.textContent = "Revisa todas las recomendaciones generadas por el sistema";
    cargarHistorial();
  }
}

function formatearFecha(fechaISO) {
  if (!fechaISO) return "Fecha no disponible";
  const fecha = new Date(fechaISO);
  return fecha.toLocaleString("es-CR");
}

function crearTagsHTML(items) {
  if (!items || items.length === 0) {
    return `<span class="history-tag">Sin datos</span>`;
  }

  return items
    .map(item => `<span class="history-tag">${item}</span>`)
    .join("");
}

function renderHistorial(consultas) {
  historyGrid.innerHTML = "";

  if (!consultas || consultas.length === 0) {
    historyGrid.classList.add("hidden");
    historyEmpty.classList.remove("hidden");
    historyEmpty.innerHTML = `
      <div class="empty-icon">📄</div>
      <h4>Aún no hay consultas registradas</h4>
      <p>Cuando generes planes de viaje, aparecerán en esta sección.</p>
    `;
    return;
  }

  historyEmpty.classList.add("hidden");
  historyGrid.classList.remove("hidden");

  const consultasOrdenadas = [...consultas].reverse();

  consultasOrdenadas.forEach(consulta => {
    const card = document.createElement("article");
    card.className = "history-card";

    card.innerHTML = `
      <h4>${consulta.usuario_nombre}</h4>
      <p class="history-date">${formatearFecha(consulta.fecha_consulta)}</p>

      <div class="history-section">
        <strong>Destinos recomendados</strong>
        <div class="history-tags">
          ${crearTagsHTML(consulta.recomendaciones)}
        </div>
      </div>

      <div class="history-section">
        <strong>Ruta sugerida</strong>
        <div class="history-tags">
          ${crearTagsHTML(consulta.ruta_sugerida)}
        </div>
      </div>

      <div class="history-section">
        <strong>Explicación</strong>
        <p>${consulta.explicacion_ia}</p>
      </div>
    `;

    historyGrid.appendChild(card);
  });
}

async function cargarHistorial() {
  historyLoading.classList.remove("hidden");
  historyGrid.classList.add("hidden");
  historyEmpty.classList.add("hidden");

  try {
    const response = await fetch(CONSULTAS_URL);

    if (!response.ok) {
      throw new Error("No se pudo cargar el historial.");
    }

    const data = await response.json();
    renderHistorial(data);
  } catch (error) {
    historyGrid.classList.add("hidden");
    historyEmpty.classList.remove("hidden");
    historyEmpty.innerHTML = `
      <div class="empty-icon">⚠️</div>
      <h4>Error al cargar el historial</h4>
      <p>${error.message || "Ocurrió un problema al obtener las consultas."}</p>
    `;
  } finally {
    historyLoading.classList.add("hidden");
  }
}

async function registrarUsuario(payload) {
  const response = await fetch(USUARIOS_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    throw new Error("No se pudo registrar el usuario.");
  }

  return await response.json();
}

async function generarPlan(payload) {
  const response = await fetch(PLANIFICAR_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    throw new Error("No se pudo generar el plan de viaje.");
  }

  return await response.json();
}

navButtons.forEach(button => {
  button.addEventListener("click", () => {
    const view = button.dataset.view;
    cambiarVista(view);
  });
});

refreshHistoryBtn.addEventListener("click", cargarHistorial);

form.addEventListener("submit", async function (event) {
  event.preventDefault();

  ocultarError();
  limpiarResultado();
  mostrarLoading();

  const nombre = document.getElementById("nombre").value.trim();
  const paises_visitados = limpiarTextoLista(
    document.getElementById("paises_visitados").value
  );
  const gustos = [document.getElementById("gustos").value];
  const presupuesto = document.getElementById("presupuesto").value;
  const clima_preferido = document.getElementById("clima_preferido").value;
  const tipo_viaje = document.getElementById("tipo_viaje").value;

  const payload = {
    nombre,
    paises_visitados,
    gustos,
    presupuesto,
    clima_preferido,
    tipo_viaje
  };

  try {
    await registrarUsuario(payload);
    const data = await generarPlan(payload);
    mostrarResultado(data);
  } catch (error) {
    mostrarError(error.message || "Ocurrió un error al procesar la solicitud.");
  } finally {
    ocultarLoading();
  }
});