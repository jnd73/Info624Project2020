document.addEventListener('DOMContentLoaded', assignClickHandler)

function assignClickHandler () {
    
    $(document).ready(function(){
      //calling of functions for adding, deleting and loading data
      $(document).on("click","#input-submit-searchbyname", searchbyName);
    });
}

function searchbyName(){
    
    $.ajax({
      url: '/searchbyName',
      method: 'POST',
      data: {
        keywords: $('#input-search').val()
      }
    })
    alert("Adding Record Complete");
    //reseting the input fields
    //document.getElementById('inputs').reset()
}