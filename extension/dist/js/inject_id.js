/*global chrome*/
const existingDiv = document.getElementById("detectedWhat");
chrome.runtime.sendMessage({ action: 'getDetectionStatus' }, function(response) {
    console.log("Current status:", response.status); 
    if (existingDiv) {
        existingDiv.innerText = response.status;
    } 
    else {
        var div = document.createElement("div");
        div.setAttribute("id", "detectedWhat");

        div.innerText = response.status;
        document.body.appendChild(div);
    }
    div.style.display = 'none';
});
