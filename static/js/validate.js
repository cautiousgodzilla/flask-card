function allLetter(inputtxt)
  {
   let letters = RegExp('^[A-Za-z]+$');

   if(letters.test(inputtxt)){
      return true;
     }
   else
     {
     return false;
     }
  }
function validatestr(event){

    elements = document.getElementsByTagName("input");
    for(var i = 0; i < elements.length; i++) {
        if (allLetter(elements[i].value) === false){
            event.preventDefault();
            alert("This value should be a string: "+ elements[i].name );
            return False
        }
    }
    return True
}