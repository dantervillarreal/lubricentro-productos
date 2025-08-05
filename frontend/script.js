document.getElementById("formulario").addEventListener("submit", async function (e) {
  e.preventDefault();

  const marca = this.marca.value;
  const modelo = this.modelo.value;
  const motor = this.motor.value;
  const anio = this.anio.value;

  const response = await fetch("http://127.0.0.1:5000/api/productos", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ marca, modelo, motor, anio })
  });

  const data = await response.json();
  const resultado = document.getElementById("resultado");
  resultado.innerHTML = ""; // Limpiar resultados anteriores

  if (Array.isArray(data) && typeof data[0] === "string") {
    resultado.innerHTML = `<p>${data[0]}</p>`;
    return;
  }

  // Crear tabla con resultados
  const table = document.createElement("table");
  table.innerHTML = `
    <thead>
      <tr>
        <th>Código</th>
        <th>Descripción</th>
        <th>Tipo</th>
        <th>Precio Unitario</th>
        <th>Stock</th>
        <th>Precio Final</th>
      </tr>
    </thead>
    <tbody>
      ${data.map(p => `
        <tr>
          <td>${p.codigo}</td>
          <td>${p.descripcion}</td>
          <td>${p.tipo}</td>
          <td>$${p.precio_unit}</td>
          <td>${p.stock}</td>
          <td>$${p.precio_final}</td>
        </tr>
      `).join("")}
    </tbody>
  `;
  resultado.appendChild(table);
});
