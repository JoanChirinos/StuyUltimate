var newTeamButton = document.getElementById('newTeamButton');
var form = document.getElementById('newTeamForm');

newTeamButton.addEventListener('click', function (e) {
  var xhr = new XMLHttpRequest();
  
  // bind form to FormData object
  var formData = new FormData(form);
  
  xhr.addEventListener('load', function () {
//    console.log(this.responseText);
    location.reload(true);
  });
  
  xhr.addEventListener('error', function (event) {
    console.log(event);
    alert('Something went wrong with team creation!');
  });
  
  xhr.open("POST", '/new_team');
  
  xhr.send(formData);
  e.preventDefault();
  e.stopImmediatePropagation();
  return false;
});