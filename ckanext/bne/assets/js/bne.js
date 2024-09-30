const params = new URLSearchParams(window.location.search)

function setParam(values){
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
  parameters = {}
  url = window.location.origin + window.location.pathname + "?" +'table=' + params.get('table') + '&'+"page=0&"
  for (const input of document.getElementsByClassName('form-control custom-input')){
    if(input.value != ""){
      parameters[input.id] = input.value
    }
  }
  for (const [key,value] of Object.entries(parameters)){
    url += key + "=" +value+'&'
  }
  window.location.replace(url)
}

function bneApiCall(apiUrl){
  fetch(apiUrl)
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    html = '<table>'
    for(entry in data['data']){
      html += bneGenerateTable(data['data'][entry])
    }
    html += '</table>'
    console.log(html)
    return html
  })
  .catch(error => {
    console.error('Error:', error);
  });
}

function bneGenerateTable(data){
  table = '<tr>'
  console.log(data)
  for(var j in data){
    table += '<td>' + data[j] + '</td>'
  }
  table += '</tr>'
  return table
}

