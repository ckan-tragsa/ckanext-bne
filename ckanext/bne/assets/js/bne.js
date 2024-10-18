const params = new URLSearchParams(window.location.search);
let page = 0;
let fields, data, table, rows, nentries, apiURLobj;

window.addEventListener('load', () => {
  // Evento que renderiza la tabla al cargar la página
  updateVars();
}, false);

function updateVars() {
  // Actualiza variables, establece el offset y renderiza la tabla y la barra de navegación
  if (!params.has('table')) {
    params.set('table', 'geo');
  }
  apiURLobj = new URL(document.getElementById('api-url').href);
  rows = parseInt(document.getElementById('bne-rows').value, 10);

  // Eliminar 'rowid' si ya existe
  apiURLobj.searchParams.delete('rowid');

  const offset = page * rows;
  apiURLobj.searchParams.append('rowid', `${rows}-${offset}`);
  const apiUrl = apiURLobj.toString();

  renderTable(apiUrl);
  bneCreateNav();
}

function setParam(values) {
  // Cambia los parámetros de URL y redirige
  const parameters = {};
  const url = new URL(window.location.origin + window.location.pathname);

  for (const [key, value] of params.entries()) {
    parameters[key] = value;
  }
  Object.assign(parameters, values);

  for (const [key, value] of Object.entries(parameters)) {
    url.searchParams.set(key, value);
  }

  window.location.replace(url.toString());
}

function formOnClick() {
  // Actualiza la tabla de la API con un conjunto dado de filtros
  const parameters = {};
  page = 0;

  const formInputs = document.querySelectorAll('.form-control.custom-input');
  formInputs.forEach(input => {
    if (input.value !== '') {
      parameters[input.id] = input.value;
    }
  });

  const baseApiUrl = `${apiURLobj.origin}/api/${params.get('table')}?`;
  const urlParams = new URLSearchParams(parameters);
  const apiUrlWithParams = `${baseApiUrl}${urlParams.toString()}`;

  // Actualizaremos 'api-url' eliminando 'rowid' si existe
  const apiURLWithParamsObj = new URL(apiUrlWithParams);
  apiURLWithParamsObj.searchParams.delete('rowid');

  const offset = page * rows;
  apiURLWithParamsObj.searchParams.append('rowid', `${rows}-${offset}`);
  const apiUrlWithRowid = apiURLWithParamsObj.toString();

  document.getElementById('api-url').href = apiUrlWithRowid;
  nentries = undefined;

  renderTable(apiUrlWithRowid);
}

async function renderTable(apiUrl) {
  // Renderiza la tabla de la API
  if (!fields) {
    await bneApiCallFields(apiUrl);
  }
  if (!nentries) {
    await bneApiCallNentries(apiUrl);
  }
  await bneApiCall(apiUrl);

  if (table) {
    table.replaceData(data);
  } else {
    initTable();
  }
}

function initTable() {
  // Inicializa la tabla Tabulator con los campos de la API
  const columns = fields.map(field => ({
    title: field.replace(/_/g, ' '),
    field: field,
  }));

  table = new Tabulator('#bne-api-table', {
    data: data,
    columns: columns,
  });

  document.getElementById('nentries').textContent = nentries;
}

async function bneApiCallFields(apiUrl) {
  // Obtiene los campos de la tabla desde la API
  const url = new URL(apiUrl);
  const apiUrlFields = `${url.protocol}//${url.host}/api/fields/${params.get('table')}`;

  try {
    const response = await fetch(apiUrlFields);
    if (!response.ok) {
      throw new Error('Error en la respuesta de la red');
    }
    const result = await response.json();
    fields = result.fields.filter(field => !field.startsWith('t_'));
  } catch (error) {
    console.error('Error al obtener los campos:', error);
  }
}

async function bneApiCall(apiUrl) {
  // Llama a la API y actualiza los datos
  try {
    const response = await fetch(apiUrl);
    if (!response.ok) {
      throw new Error('Error en la respuesta de la red');
    }
    const result = await response.json();
    data = result.data;
  } catch (error) {
    console.error('Error al obtener los datos:', error);
  }
}

async function bneApiCallNentries(apiUrl) {
  // Obtiene el número de entradas para la paginación
  const apiUrlCountObj = new URL(apiUrl);
  apiUrlCountObj.searchParams.set('count', '1');
  const apiUrlCount = apiUrlCountObj.toString();

  try {
    const response = await fetch(apiUrlCount);
    if (!response.ok) {
      throw new Error('Error en la respuesta de la red');
    }
    const result = await response.json();
    nentries = result.data[0].id;
    document.getElementById('nentries').textContent = nentries;
    bneCreateNav();
  } catch (error) {
    console.error('Error al obtener el número de entradas:', error);
  }
}

function bneCreateNav() {
  // Crea la barra de navegación inferior basada en el número de entradas y la página actual
  const nav = document.getElementById('api-nav');
  let html = '';
  const totalPages = Math.ceil(nentries / rows);

  const createPageButton = (pageNumber, isCurrent = false) => {
    if (isCurrent) {
      return `<div class="current-page">${pageNumber}</div>`;
    } else {
      return `<input type="button" value="${pageNumber}" onclick="page=${pageNumber}; updateVars()">`;
    }
  };

  if (page < 5) {
    for (let i = 0; i <= page; i++) {
      html += createPageButton(i, i === page);
    }
  } else {
    html += createPageButton(0);
    html += '<div>...</div>';
    for (let i = page - 2; i < page; i++) {
      html += createPageButton(i);
    }
    html += createPageButton(page, true);
  }

  if (totalPages - page < 5) {
    for (let i = page + 1; i < totalPages; i++) {
      html += createPageButton(i);
    }
  } else {
    for (let i = page + 1; i <= page + 3; i++) {
      html += createPageButton(i);
    }
    html += '<div>...</div>';
    html += createPageButton(totalPages - 1);
  }

  nav.innerHTML = html;
}