// users.js - Manejo del toggle para agregar usuario
document.addEventListener('DOMContentLoaded', () => {
  const toggleBtn = document.getElementById('btn-toggle-add');
  const formAdd = document.getElementById('form-add-user');
  const form = document.getElementById('form-add-user');
  const inputNombre = form ? form.querySelector('input[name="nombre"]') : null;

  // Toggle del formulario
  if (toggleBtn && formAdd) {
    toggleBtn.addEventListener('click', (event) => {
      event.preventDefault();
      formAdd.classList.toggle('hidden');
      const isVisible = !formAdd.classList.contains('hidden');
      if (isVisible) {
        formAdd.classList.add('visible');
        toggleBtn.textContent = '✖ Cerrar';
      } else {
        formAdd.classList.remove('visible');
        toggleBtn.textContent = '➕ Nuevo usuario';
      }
    });
  }

  // Validación del formulario
  if (form) {
    form.addEventListener('submit', (event) => {
      const nombre = inputNombre ? inputNombre.value.trim() : '';
      if (!nombre) {
        event.preventDefault();
        alert('Por favor, ingresa un nombre válido para el usuario.');
        inputNombre.focus();
        return false;
      }
      if (nombre.length < 2) {
        event.preventDefault();
        alert('El nombre debe tener al menos 2 caracteres.');
        inputNombre.focus();
        return false;
      }
    });
  }
});