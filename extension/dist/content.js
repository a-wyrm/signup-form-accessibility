function sendPageSignals() {
  const pageSignals = getSignalsAndConvertToBinary();

  chrome.runtime.sendMessage({ messageType: "page_signals", pageSignals }, (response) => {
    console.log("Sent page signals.");
    console.log('received user data', response);

    var existingDiv = document.getElementById("detectedWhat");
    if (existingDiv){
        existingDiv.remove();
    }
    var div = document.createElement("div");
    div.setAttribute("id", "detectedWhat");
    div.innerText = JSON.stringify(response);
    div.style.display = 'none';
    document.body.appendChild(div);
    
  });

}

// On page load, send the page signals to the background script
window.addEventListener("load", function () {
  setTimeout(sendPageSignals, 2000);
});

// On single page applications, the page load event is not triggered, so we need to listen to the message from the background script
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.action === 'pageUpdated') {
    // Send the extracted information to the background script
    setTimeout(sendPageSignals, 2000);
    }
  });



