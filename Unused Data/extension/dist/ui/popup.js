/*global chrome*/
let currentTab;

function updatePageType(){
  let pageTypeText = "";
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    currentTab = tabs[0];
    const tabId = currentTab.id;
    console.log("currentTab", tabId);
    const tabIdStr = tabId.toString();
    chrome.storage.local.get([tabIdStr], function (results) {
      let result = results[tabIdStr];
      if (result.isLogin) {
        pageTypeText = "Detected Login page.";
        document.getElementById("ml_result").innerHTML = pageTypeText;
      } else if (result.isSignup) {
        pageTypeText = "Detected Signup page.";
        document.getElementById("ml_result").innerHTML = pageTypeText;
      } else {
        pageTypeText = "No data found for this page.";
        document.getElementById("ml_result").innerHTML = pageTypeText;
      }
    });
    
    chrome.tabs.sendMessage(currentTab.id, { action: "createDiv", pageTypeText });
  });

}

updatePageType();


chrome.runtime.onMessage.addListener(function (msg, sender, sendResponse) {
  if (msg.messageType === "page_storage_cleared") {
    updatePageType();
  }
});

