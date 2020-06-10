// Before refreshing the page, save the form data to sessionStorage
window.onbeforeunload = function() {
  sessionStorage.setItem("country_selected", $('#country_selected').val());
  sessionStorage.setItem("state_selected", $('#state_selected').val());
}

function hideLoader() {
    $('#image').css("display", "none");
}

function showLoader() {
    $('#image').css("display", "block");
}

hideLoader();

$("#country_selected").change(function () {
  showLoader();
  var prev_country = sessionStorage.getItem("country_selected");
  var prev_state = sessionStorage.getItem("state_selected");
  var country = $(this).val();
  var state = $("#state_selected").val();
  $.ajax({
    url: '/ajax/get_country/',
    cache: false,
    async : false, //must set async to false
    beforeSend: function() {
        showLoader();
    },
    data: {
      'country': country,
      'state': state
    },
    dataType: 'json'
    })
    .done(function(data, textStatus, jqxhr){
        if (prev_country != country || prev_state != state) {
          $('#timeseries').html(data.fileContent);
          document.getElementById('ratios_div').innerHTML = "<br/>Total <b>confirmed</b> cases in this <b>country</b> : <b>" + data.ratios.total_confirmed + "</b>" +
                                                            "<br/>Total <b>deaths</b> in this <b>country</b>: <b>" + data.ratios.total_deaths + "</b>" +
                                                            "<br/>Total people <b>recovered</b> this <b>country</b>: <b>" + data.ratios.total_recover + "</b>" +
                                                            "<br/>Total <b>confirmed</b> cases in this <b>state</b>: <b>" + data.ratios.state_total_confirmed + "</b>" +
                                                            "<br/>Total <b>deaths</b> in this <b>state</b>: <b>" + data.ratios.state_total_deaths + "</b>" +
                                                            "<br/>Total people <b>recovered</b> in this <b>state</b>: <b>" + data.ratios.state_total_recover + "</b>" +
                                                            "<br/>Fatality Ratio: " + data.ratios.fatality_ratio +
                                                            "<br/>Recovery Proficiency Ratio: " + data.ratios.recovery_prof_ratio +
                                                            "<br/>"+
                                                            "<br/>Predicted number of cases till next week: " + data.ratios.cases_predicted +
                                                             "<br/><br/>***<br/> Risk Ratio: Probability of an individual getting infected by the virus"+
                                                             " within that region (Confirmed Cases / Population) <br/>" +
                                                             "Fatality Ratio: Measure of a disease's severity in that region (Total cases of death / Total confirmed cases) <br/>"+
                                                             "Recovery Proficiency Ratio: Total Recovered cases out of total affected cases in that region <br/>";
        }
        hideLoader();
    })
    .fail(function(jqxhr, data, errorThrown){
        console.log(data)
        console.log(errorThrown);
        hideLoader()
    });
});

$("#state_selected").change(function () {
  showLoader();
  var prev_country = sessionStorage.getItem("country_selected");
  var prev_state = sessionStorage.getItem("state_selected");
  var country = $("#country_selected").val();
  var state = $(this).val();
  $.ajax({
    url: '/ajax/getcountry_state/',
    data: {
      'country': country,
      'state': state
    },
    dataType: 'json'
    })
    .done(function(data, textStatus, jqxhr){

      if (prev_country != country || prev_state != state) {
        $('#timeseries').html(data.fileContent);
        document.getElementById('ratios_div').innerHTML = "<br/>Total <b>confirmed</b> cases in this <b>country</b> : <b>" + data.ratios.total_confirmed + "</b>" +
                                                            "<br/>Total <b>deaths</b> in this <b>country</b>: <b>" + data.ratios.total_deaths + "</b>" +
                                                            "<br/>Total people <b>recovered</b> this <b>country</b>: <b>" + data.ratios.total_recover + "</b>" +
                                                            "<br/>Total <b>confirmed</b> cases in this <b>state</b>: <b>" + data.ratios.state_total_confirmed + "</b>" +
                                                            "<br/>Total <b>deaths</b> in this <b>state</b>: <b>" + data.ratios.state_total_deaths + "</b>" +
                                                            "<br/>Total people <b>recovered</b> in this <b>state</b>: <b>" + data.ratios.state_total_recover + "</b>" +
                                                            "<br/>Fatality Ratio: " + data.ratios.fatality_ratio +
                                                            "<br/>Recovery Proficiency Ratio: " + data.ratios.recovery_prof_ratio +
                                                            "<br/>"+
                                                            "<br/>Predicted number of cases till next week: " + data.ratios.cases_predicted +
                                                             "<br/><br/>***<br/> Risk Ratio: Probability of an individual getting infected by the virus"+
                                                             " within that region (Confirmed Cases / Population) <br/>" +
                                                             "Fatality Ratio: Measure of a disease's severity in that region (Total cases of death / Total confirmed cases) <br/>"+
                                                             "Recovery Proficiency Ratio: Total Recovered cases out of total affected cases in that region <br/>";
      }
    hideLoader();
    })
    .fail(function(jqxhr, data, errorThrown){
        console.log(errorThrown);
    });
});
