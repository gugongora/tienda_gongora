document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("converter-form");
  if (!form) return;

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const monto = parseFloat(document.getElementById("monto-usd").value);
    const resultado = document.getElementById("resultado");
    const error = document.getElementById("error");

    resultado.style.display = "none";
    error.style.display = "none";

    if (isNaN(monto) || monto <= 0) {
      error.innerText = "Por favor ingresa un monto válido.";
      error.style.display = "block";
      return;
    }

    fetch(`/conversion/convertir/?monto=${monto}`)
      .then((response) => response.json())
      .then((data) => {
        if (data.monto_clp !== undefined) {
          resultado.innerHTML = `
            <strong>Valor del dólar:</strong> ${data.valor_dolar_clp} CLP<br>
            <strong>Resultado:</strong> ${data.monto_usd} USD = ${data.monto_clp} CLP
          `;
          resultado.style.display = "block";
        } else if (data.error) {
          error.innerText = data.error;
          error.style.display = "block";
        }
      })
      .catch(() => {
        error.innerText = "Error al conectar con el servidor.";
        error.style.display = "block";
      });
  });
});
