


function createCheckboxElement(metricName, hostData, className) {
  var $checkbox = $("<input type='checkbox' id='" + metricName + "' value='" + metricName +"'>");
  var $label = $("<label for='" + metricName + "'>" + hostData.name + "</label>");
  var $divs = $("<ul class='" + className +"'>");

  var $li = $('<li id="popup" class="info-popup"></div>')
  $divs.append($li);

  $divs.on('mouseover', function() {
    $li.text(hostData.desc); // Set popup content
    $li.addClass('show'); // Show the popup on hover
  });
  $divs.on('mouseout', function() {
    $li.removeClass('show'); // Hide the popup on mouseout
  });

  $divs.append($checkbox, $label);
  return $divs;
}


fetch('./metric.json')
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
    const thisVal = (this.checked ? data.push(labelText) : "");
  });
  console.log(data);

  const csvContent = data.map(item => `${item.label}`).join('\n');
  const blob = new Blob([csvContent], { type: 'text/csv' });
  
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'data.csv';

  a.click();

}