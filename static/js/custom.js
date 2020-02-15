function setSelectedValue(value ,top) {
  var country_state = JSON.parse(JSON.stringify( top ));
  if (value.length == 0) document.getElementById("state_selected").innerHTML = "<option></option>";
  else {
    var catOptions = "";
    for (state in country_state[value]) {
        catOptions += "<option selected='selected'>" + country_state[value][state] + "</option>";
    }
    document.getElementById("state_selected").innerHTML = catOptions;
  }
}