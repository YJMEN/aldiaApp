// common.js - Funciones comunes de JavaScript para el frontend

// Confirmación de logout
function confirmLogout() {
  const logoutBtn = document.querySelector('a[href*="logout"]');
  if (logoutBtn) {
    logoutBtn.addEventListener("click", async (e) => {
      e.preventDefault();
      const result = await Swal.fire({
        title: "¿Cerrar sesión?",
        text: "¿Estás seguro de que quieres cerrar sesión?",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#3b82f6",
        cancelButtonColor: "#94a3b8",
        confirmButtonText: "Sí, cerrar",
        cancelButtonText: "Cancelar",
        background: "#11192b",
        color: "#e2e8f0",
      });
      if (result.isConfirmed) {
        window.location.href = "/logout";
      }
    });
  }
}

// Confirmación de submit de formularios
function confirmFormSubmit(
  formSelector,
  title,
  text,
  confirmText = "Sí, confirmar",
) {
  const form = document.querySelector(formSelector);
  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const result = await Swal.fire({
        title: title,
        text: text,
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#3b82f6",
        cancelButtonColor: "#94a3b8",
        confirmButtonText: confirmText,
        cancelButtonText: "Cancelar",
        background: "#11192b",
        color: "#e2e8f0",
      });
      if (result.isConfirmed) {
        form.submit();
      }
    });
  }
}

// Confirmación de reset
function confirmReset(formSelector) {
  confirmFormSubmit(
    formSelector,
    "¿Reiniciar todo?",
    "Esto eliminará todos los usuarios y pagos. ¿Estás seguro?",
    "Sí, reiniciar",
  );
}

// Confirmación de agregar usuario
function confirmAddUser(formSelector) {
  const form = document.querySelector(formSelector);
  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const nombre = form.querySelector('input[name="nombre"]').value.trim();
      if (!nombre) {
        await Swal.fire({
          icon: "warning",
          title: "Campo vacío",
          text: "Por favor, ingresa un nombre para el usuario.",
          confirmButtonText: "Entendido",
          background: "#11192b",
          color: "#e2e8f0",
          confirmButtonColor: "#3b82f6",
        });
        return;
      }
      const result = await Swal.fire({
        title: "¿Registrar usuario?",
        text: `¿Confirmas registrar a "${nombre}" como nuevo usuario?`,
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#3b82f6",
        cancelButtonColor: "#94a3b8",
        confirmButtonText: "Sí, registrar",
        cancelButtonText: "Cancelar",
        background: "#11192b",
        color: "#e2e8f0",
      });
      if (result.isConfirmed) {
        form.submit();
      }
    });
  }
}

// Confirmación de pago
function confirmPago() {
  document.querySelectorAll(".pago-form").forEach((form) => {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const tipo = form.querySelector('select[name="tipo_pago"]').value;
      const parcial = form.querySelector('input[name="valor_parcial"]').value;

      if (!tipo) {
        await Swal.fire({
          icon: "warning",
          title: "Selecciona tipo",
          text: "Elige si el pago es completo o parcial.",
          confirmButtonText: "Entendido",
          background: "#11192b",
          color: "#e2e8f0",
          confirmButtonColor: "#3b82f6",
        });
        return;
      }

      let mensaje =
        tipo === "completo"
          ? "¿Confirmas pago completo?"
          : `¿Confirmas pago parcial de ${parcial}?`;

      const result = await Swal.fire({
        title: "Confirmar pago",
        text: mensaje,
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#3b82f6",
        cancelButtonColor: "#94a3b8",
        confirmButtonText: "Sí, registrar",
        cancelButtonText: "Cancelar",
        background: "#11192b",
        color: "#e2e8f0",
      });

      if (result.isConfirmed) {
        form.submit();
      }
    });
  });
}

// Inicializar funciones comunes al cargar la página
document.addEventListener("DOMContentLoaded", () => {
  confirmLogout();
});
