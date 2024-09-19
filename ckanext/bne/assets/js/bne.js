// When the user scrolls the page, execute myFunction
window.onscroll = function() {myFunction()};

// Get the header
var header = document.getElementsByClassName("masthead")[0];
console.log(header)

// Get the offset position of the navbar
var sticky = header.offsetTop;

// Add the sticky class to the header when you reach its scroll position. Remove "sticky" when you leave the scroll position
function myFunction() {
  if (window.scrollY > sticky) {
    header.classList.add("sticky");
  } else {
    header.classList.remove("sticky");
  }
} 

const params = new URLSearchParams(window.location.search)

function setParam(key, value){
  parameters = {}
  url = window.location.origin + window.location.pathname + "?"
  for (const key of params.keys()) {
    parameters[key] = params.get(key)
  }
  parameters[key] = value
  for (const [key,value] of Object.entries(parameters)){
    url += key + "=" +value+'&'
  }
  window.location.replace(url)
}

function getParam(key){
  if(params.has(key)) {
      return params.get(key)
  }else{
      return ""
  }
}

function formOnClick(){
  parameters = {}
  url = window.location.origin + window.location.pathname + "?" +'table=' + params.get('table') + '&'+"page=0&"
  for (const input of document.getElementsByClassName('filters-input')){
    if(input.value != ""){
      parameters[input.id] = input.value
    }
  }
  for (const [key,value] of Object.entries(parameters)){
    url += key + "=" +value+'&'
  }
  window.location.replace(url)
}


