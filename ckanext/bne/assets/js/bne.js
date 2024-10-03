const params = new URLSearchParams(window.location.search)
var page = 0
var fields, data, table, rows, nentries, apiURLobj

window.addEventListener("load", function() {
  /**
   * event that renders the table on first load
   */
  updateVars()
},false); 


function updateVars(){
  /**
   * Function that updates variables, sets the offset and calls for the rendering of the nav bar and table
   * It runs at every table update
   */
  if(params.get('table') == null ){
    params.set('table','geo')
  }
  apiURLobj = new URL(document.getElementById('api-url').href)
  rows = document.getElementById('bne-rows').value
  //update table
  let offset = page * rows
  let apiUrl = apiURLobj.href + "&rowid=" + rows +"-"+ offset
  renderTable(apiUrl)
  bneCreateNav()
}

function setParam(values){
    /**
     * changes url parameters and redirects
     */
    parameters = {}
    url = window.location.origin + window.location.pathname + "?"
    for (const key of params.keys()) {
      parameters[key] = params.get(key)
    }
    for(const [key,value] of Object.entries(values)){
      parameters[key] = values[key]
    }
    for (const [key,value] of Object.entries(parameters)){
      url += key + "=" +value+'&'
    }
    window.location.replace(url)
}




function formOnClick(){
  /**
   * function that updates API table with a given ser of filters
   * input:
   */
  parameters = {}
  
  page = 0;
  let url = apiURLobj.origin + '/api/' + params.get('table') + '?'
  for (const input of document.getElementsByClassName('form-control custom-input')){
    if(input.value != ""){
      parameters[input.id] = input.value
    }
  }
  for (const [key,value] of Object.entries(parameters)){
    url += '&' + key + "=" +value
  }
  document.getElementById('api-url').href = url
  let offset = page * rows
  url += "&rowid=" + rows +"-"+ offset
  nentries = undefined
  renderTable(url)
}

function renderTable(apiUrl){
  /**
   * renders api table 
   */
  if(!fields){
    bneApiCallFields(apiUrl)
  }
  if(!nentries){
    bneApiCallNentries(apiUrl+"&count=1")
  }
  bneApiCall(apiUrl) 
  if(table){
    setTimeout(renderTableAux(),100)
  }else{
    initTable()
  }

}

function renderTableAux(){
  /**
   * Function that waits for data to be received and updates table data
   */
  if(data != undefined ){
    table.replaceData(data)
  }else{
    setTimeout(renderTableAux,100)
  }
}

function initTable(){
  /**
   * function that waits for data to be received and initializes tabulator table with api fields
   */
  if(data != undefined){
    let field = ""
    let columns = []
    for(var i in fields){
      field = fields[i].replace(/[_]/g," ")
      columns.push({
        title:field,
        field:fields[i]
      })
    }
    table = new Tabulator("#bne-api-table",{
      data:data, 
      columns:columns
    })
    document.getElementById('nentries').innerHTML = nentries
  }else{
    setTimeout(initTable,100)
  }
}

function bneApiCallFields(apiUrl){
  /**
   * function that gets the table fields from the API 
   * input:
   *  baseURL: String with the API url href
   */
  const url = new URL(apiUrl)
  const apiUrlcropped = url.protocol + '//' + url.host + "/api/fields/" + params.get('table') 
  fetch(apiUrlcropped)
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    fieldsCropped = []
    for(const i in data['fields']){
      if('t_' != data['fields'][i].substring(0,2)){
        fieldsCropped.push(data['fields'][i])
      }
    }
    fields = fieldsCropped
   })
  .catch(error => {
    console.error('Error:', error);
  });
}

function bneApiCall(apiUrl){
  /**
   * Calls api and adds values to a table 
   * input:
   *  baseURL: String with the API url href
   */
  data = undefined
  fetch(apiUrl)
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    this.data = data['data']
   })
  .catch(error => {
    console.error('Error:', error);
  });
}

function bneApiCallNentries(apiUrl){
  /**
   * Calls api and adds values to a table 
   * input:
   *  baseURL: String with the API url href
   */
  data = undefined
  apiUrl += "&count=1"
  fetch(apiUrl)
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    nentries = data['data'][0]['id']
    document.getElementById('nentries').innerHTML = nentries
    bneCreateNav()
   })
  .catch(error => {
    console.error('Error:', error);
  });
}

function bneCreateNav(){
  /**
   * Creates bottom nav bar based on the number of entries and the current page
   */
  let nav = document.getElementById('api-nav')
  let html = ''
  let pages = Math.ceil(nentries/rows)

  // Renders 
  if(page < 5){
    for(var i in Array.from(Array(page+1).keys())){
      if(i == page ){
        html += '<div class="current-page">'+page+'</div>'
      }else{
        html += '<input type="button" value="'+i+'"onclick="page='+i+'; updateVars()">'
      }
    }
  }else{
    html += '<input type="button" value="0"onclick="page=0; updateVars()">'
    html += '<div>...</div>'
    for(var i in Array.from(Array(3).keys())){
      j = page+Number(i)-3
      html += '<input type="button" value="'+j+'"onclick="page='+j+'; updateVars()">'      
    }
    html += '<div class="current-page">'+page+'</div>'
  }
  if(pages-page < 5){
    for(var i in Array.from(Array(pages-page).keys())){
      let j = page + Number(i)
      if(j != page ){
        html += '<input type="button" value="'+j+'"onclick="page='+j+'; updateVars()">'
      }
    }
  }else{
    for(var i in Array.from(Array(3).keys())){
        let j = Number(i)+page+1
        html += '<input type="button" value="'+j+'"onclick="page='+j+'; updateVars()">'
    }
    html += '<div>...</div>'
    html += '<input type="button" value="'+(pages-1)+'"onclick="page='+(pages-1)+'; updateVars()">'
  }
  nav.innerHTML = html
}