
var existingDiv = document.getElementById("detectedWhat");
chrome.runtime.sendMessage({ action: 'getDetectionStatus' }, function(response) {
    console.log("Current status:", response.status); 
    if (existingDiv) {
        existingDiv.innerText = response.status;
    }
});
