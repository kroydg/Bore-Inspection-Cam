var configData = {}; 
// prepare html dom elements 
var expDisplay = document.getElementById("expDisplay");
var briDisplay = document.getElementById("briDisplay");
var expInput = document.getElementById("expInput"); 
var expButton = document.getElementById("saveExp");
var briInput = document.getElementById("briInput"); 
var briButton = document.getElementById("savebrightness");
// create a http (Rest) GET request 
// auto infer base url because on same origin 
const url = "/configData"; 
// Initialize HTTP reqest 
const getConfigRequest = new XMLHttpRequest(); 
getConfigRequest.open("GET", url);
getConfigRequest.send();


getConfigRequest.onreadystatechange = (e) => {
    if (getConfigRequest.status == 200) { 
        const textData = getConfigRequest.responseText;
        // Parse text based json into Object
        const parsedData = JSON.parse(textData); 
        configData = parsedData;
        expDisplay.innerHTML = parsedData.exposure; 
        briDisplay.innerHTML = parsedData.brightness;
    }

    
}
expButton.addEventListener("click", () => {

        configData.exposure = expInput.value;
        const postConfigRequest = new XMLHttpRequest(); 
        postConfigRequest.open("POST", url);
        const reqBody = { configData: {}};
        reqBody.configData = configData;
        postConfigRequest.setRequestHeader("Content-Type", "application/json");
        postConfigRequest.send(JSON.stringify(reqBody));
        postConfigRequest.onreadystatechange = (e) => {
                if (postConfigRequest.status == 200 &&  expInput.value!=null) {
                    expDisplay.innerHTML = configData.exposure; 
                    expInput.value = ""; 
                }
                else {
                    alert("save failed !");
                }
        }
    
});
briButton.addEventListener("click", () => {

        configData.brightness = briInput.value;
        const postConfigRequest = new XMLHttpRequest(); 
        postConfigRequest.open("POST", url);
        const reqBody = { configData: {}};
        reqBody.configData = configData;
        postConfigRequest.setRequestHeader("Content-Type", "application/json");
        postConfigRequest.send(JSON.stringify(reqBody));
        postConfigRequest.onreadystatechange = (e) => {
                if (postConfigRequest.status == 200 ) {
                    briDisplay.innerHTML = configData.brightness; 
                    briInput.value = ""; 
                }
                else {
                    alert("save failed !");
                }
        }

}); 


console.log("Hey, York created me");