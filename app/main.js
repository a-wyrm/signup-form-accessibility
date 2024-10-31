


function createCheckboxElement(metricName, hostData, className) {
  var $checkbox = $("<input type='checkbox' id='" + metricName + "' value='" + metricName +"'>");
  var $label = $("<label for='" + metricName + "'>" + hostData.name + "</label>");
  var $divs = $("<div class='" + className +"'>");

  var $descDiv = $("<div class='desc'>" + hostData.desc + "</div>");

  /*   var $li = $('<li id="popup" class="info-popup"></div>')
    $divs.append($li);

    $divs.on('mouseover', function() {
      $li.text(hostData.desc); // Set popup content
      $li.addClass('show'); // Show the popup on hover
    });
    $divs.on('mouseout', function() {
      $li.removeClass('show'); // Hide the popup on mouseout
    });
  */

  $divs.append($checkbox, $label, $descDiv);
  return $divs;
}


fetch('./metric.json')
  .then(response => response.json())
  .then(data => {
    Object.entries(data).forEach(([metricName, hostData]) => {
      const $checkboxDiv = createCheckboxElement(metricName, hostData, 'checkbox-space');
      $('.checkbox-container').append($checkboxDiv);

      const $descDiv = createCheckboxElement(metricName, hostData.desc , 'checkbox-space');
      $('desc-container').append($descDiv);
    });
  })
  .catch(error => {
    console.error("Error fetching JSON:", error);
  });

fetch('./password_managers.json')
  .then(response => response.json())
  .then(data => {
    Object.entries(data).forEach(([metricName, hostData]) => {
      const $checkboxDiv = createCheckboxElement(metricName, hostData, 'checkbox-space');
      $('.checkbox-container').append($checkboxDiv);
    });
  })
  .catch(error => {
    console.error("Error fetching JSON:", error);
  });



function exportToCSV() {
  const data = [];
  $('input[type=checkbox]').each( function () {
    var labelText = $(this).next().text();
    this.checked ? data.push(labelText) : "";
  });

  const grab_text = $('#issues_box').val();
  var csvContent = data.map(item => `${item}`).join('\n');
  const blob = new Blob([csvContent, '\n', "Other issues: " + grab_text], { type: 'text/csv' });
  
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'data.csv';

  a.click();

}