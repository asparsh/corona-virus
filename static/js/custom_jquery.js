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
          document.getElementById('ratios_div').innerHTML = "<br/>Risk Ratio: " + data.ratios.risk_ratio +
                                                            "<br/>Fatality Ratio: " + data.ratios.fatality_ratio +
                                                            "<br/>Recovery Proficiency Ratio: " + data.ratios.recovery_prof_ratio +
                                                            "<br/>Cases Till date: " + data.ratios.cases_till_date +
                                                            "<br/>Predicted number of cases till next week: " + data.ratios.cases_predicted +
                                                            "<br/><br/>***<br/> Risk Ratio: Total confirmed cases in region / Total Population <br/>" +
                                                                    "Fatality Ratio: Total deaths cases in region / Total confirmed cases <br/>"+
                                                                    "Recovery Ratio: Total Recovered cases in region / Total confirmed cases <br/>";
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
        document.getElementById('ratios_div').innerHTML = "<br/>Risk Ratio: " + data.ratios.risk_ratio +
                                                            "<br/>Fatality Ratio: " + data.ratios.fatality_ratio +
                                                            "<br/>Recovery Proficiency Ratio: " + data.ratios.recovery_prof_ratio +
                                                            "<br/>Cases Till date: " + data.ratios.cases_till_date +
                                                            "<br/>Predicted number of cases till next week: " + data.ratios.cases_predicted +
                                                            "<br/><br/>***<br/> Risk Ratio is: Total confirmed cases in region / Total Poputaltion <br/>" +
                                                                    "Fatality Ratio is: Total deaths cases in region / Total confirmed cases <br/>"+
                                                                    "Recovery Ration is: Total Recovered cases in region / Total confirmed cases <br/>";
      }
    hideLoader();
    })
    .fail(function(jqxhr, data, errorThrown){
        console.log(errorThrown);
    });
});
