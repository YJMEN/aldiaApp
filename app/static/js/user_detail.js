// user_detail.js - Manejo de pagos y formularios
document.addEventListener('DOMContentLoaded', () => {
  // Toggle para botones de pagar con animación
  document.querySelectorAll('.btn-pagar').forEach(button => {
    button.addEventListener('click', () => {
      const pagoId = button.dataset.pagoId;
      const form = document.getElementById(`form-pago-${pagoId}`);
      if (form) {
        form.classList.toggle('hidden');
        const isVisible = !form.classList.contains('hidden');
        if (isVisible) {
          form.classList.add('visible');
        } else {
          form.classList.remove('visible');
        }
      }
    });
  });

  // Manejo de selects en formularios de pago
  document.querySelectorAll('.pago-form').forEach(form => {
    const tipoSelect = form.querySelector('select[name="tipo_pago"]');
    const parcialInput = form.querySelector('input[name="valor_parcial"]');
    const submitBtn = form.querySelector('button[type="submit"]');

    if (tipoSelect && parcialInput) {
      tipoSelect.addEventListener('change', () => {
        if (tipoSelect.value === 'completo') {
          parcialInput.value = '';
          parcialInput.disabled = true;
          parcialInput.style.opacity = '0.5';
        } else {
          parcialInput.disabled = false;
          parcialInput.style.opacity = '1';
          parcialInput.focus();
        }
      });
    }

    // Validación del formulario de pago
    if (form) {
      form.addEventListener('submit', (event) => {
        const tipo = tipoSelect ? tipoSelect.value : '';
        const valorParcial = parcialInput ? parcialInput.value.trim() : '';

        if (!tipo) {
          event.preventDefault();
          alert('Selecciona el tipo de pago.');
          tipoSelect.focus();
          return false;
        }

        if (tipo === 'parcial') {
          if (!valorParcial) {
            event.preventDefault();
            alert('Ingresa un valor para el pago parcial.');
            parcialInput.focus();
            return false;
          }
          const valorNum = parseFloat(valorParcial);
          if (isNaN(valorNum) || valorNum <= 0) {
            event.preventDefault();
            alert('El valor parcial debe ser un número positivo.');
            parcialInput.focus();
            return false;
          }
          if (valorNum > 12000) {
            event.preventDefault();
            parcialInput.focus();
            return false;
          }
        }
      });
    }
  });
});