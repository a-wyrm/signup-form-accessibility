/*global chrome*/
var existingDiv = document.getElementById("detectedWhat");
if (existingDiv){
    existingDiv.remove();
}
var div = document.createElement("div");
div.setAttribute("id", "detectedWhat");
div.innerText = "None";
div.style.display = 'none';
document.body.appendChild(div);
