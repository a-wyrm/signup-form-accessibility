// Loop through items in JSON data.
fetch('./metric.json')
  .then(response => response.json())
  .then(data => {
    Object.entries(data).forEach(function([metricName, hostData]) {

  var $checkbox = $("<input type='checkbox' id='" + metricName + "' value='" + metricName +"'>");
  var $label = $("<label for='" + metricName + "'>" + hostData.name + "</label>");
  var $divs = $("<div class='checkbox-space'></div>");
  $divs = $divs.append($checkbox, $label);
  $('.checkbox-container').append($divs);

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