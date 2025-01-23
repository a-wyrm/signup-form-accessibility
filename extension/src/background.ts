import * as tf from "@tensorflow/tfjs";

const model_path = "model/login_signup_classifier.json";
let model: tf.GraphModel<string | tf.io.IOHandler>;
async function loadModel(path: string) {
  console.log("Model loading in progress from ".concat(path));
  const model = await tf.loadGraphModel(path);
  return model;
}

/**
 * Retrieve the array key corresponding to the largest element in the array.
 *
 * @param {Array.<number>} array Input array
 * @return {number} Index of array element with largest value
 */
function argMax(array: number[]) {
  return array
    .map((x: any, i: any) => [x, i])
    .reduce((r: number[], a: number[]) => (a[0] > r[0] ? a : r))[1];
}

const keepAlive = () => setInterval(chrome.runtime.getPlatformInfo, 20e3);
chrome.runtime.onStartup.addListener(keepAlive);
keepAlive();

chrome.runtime.onInstalled.addListener(async function () {
  model = await loadModel(model_path);
  console.log("Model Loaded Successfully");
  return true;
});

// On single page application, the page is not reloaded, so we need to listen to history state change
chrome.webNavigation.onHistoryStateUpdated.addListener(function(details) {
  chrome.tabs.sendMessage(details.tabId, { action: 'pageUpdated' });
});


function sendInjection(){
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    var currentTab = tabs[0];
    const tabId = currentTab.id || '';

    // inject script
    chrome.scripting.executeScript({
      target: { tabId: tabId || 0, allFrames: true },
      files: ['js/inject_id.js'],
    });

  });
}

chrome.runtime.onMessage.addListener(function (msg, sender, sendResponse) {
  let tabId = sender?.tab?.id;
  if (tabId) {
    const tabIdStr = tabId.toString();
    chrome.runtime.sendMessage(
      { messageType: "page_storage_cleared" },
      function (response) {
        if (!chrome.runtime.lastError) {
          console.log("Page type data cleared");
        }
      }
    );
    if (msg.messageType === "page_signals") {
      const res = predict(msg.pageSignals);
      if (res.sendMessage) {
        chrome.storage.local.set({ [tabId]: res }, function () {
          console.log("Page type data saved");
          sendInjection();
          chrome.runtime.onMessage.addListener(
            function(request, sender, sendResponse) {
              if (request.action === 'getDetectionStatus') {
                console.log(res)
                sendResponse({ status: JSON.stringify(res) });           
              }
            }
          );
        });
      }
    }
  }
  Promise.resolve("").then((result) => sendResponse(result));
  return true;
});


chrome.tabs.onUpdated.addListener(function (tabId, info) {
  if (info.status === "loading") {
    chrome.storage.local.set(
      { [tabId]: { isLogin: false, isSignup: false } },
      function () {
        console.log("Page type storage cleared.");
        chrome.scripting.executeScript({
          target: { tabId: tabId || 0, allFrames: true },
          files: ['js/inject_tag.js'],
        });
      }
    );
    chrome.runtime.sendMessage(
      { messageType: "page_storage_cleared" },
      function (response) {
        if (!chrome.runtime.lastError) {
          console.log("Page type data cleared");
        }
      }
    );
  }
});

function predict(pageSignals: number[]) {
  let result = { isLogin: false, isSignup: false, sendMessage: true };
  const res = model.predict([tf.tensor([pageSignals])]) as tf.Tensor;
  const res_arr = res.dataSync();
  const res_argmax = argMax(Array.from(res_arr));
  if (res_argmax === 0) {
    result.sendMessage = false;
  } else if (res_argmax === 1) {
    result.isLogin = true;
  } else if (res_argmax === 2) {
    result.isSignup = true;
  }
  return result;
}
