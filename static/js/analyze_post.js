"use strict";

function showToneData (toneData) {
    for (const data of toneData) {
            const newDiv = document.createElement("div");
                const hexValue = document.createElement("div")
                    hexValue.style.backgroundColor=data.hex_value;
                    hexValue.style.borderRadius="100%";
                    hexValue.style.height="20px"; 
                    hexValue.style.width="20px";
                    hexValue.style.float="left";
                    newDiv.append(hexValue);
                const padding1 = document.createElement("div") 
                    padding1.style.paddingRight="20px"
                    padding1.style.display="inline-block";
                    newDiv.append(padding1)   
                const toneQuality = document.createTextNode(data.tone_quality +  "     ");
                    newDiv.append(toneQuality);
                const toneScore = document.createTextNode(data.tone_score + "%");
                    newDiv.append(toneScore);
            const currentDiv = document.getElementById('post_tone');
            currentDiv.appendChild(newDiv);
    }    
}

const toneAnalysis = `/api/tone/${postID}`; 

fetch(toneAnalysis)
.then((response) => response.json())
.then((toneData) => {
    console.log(toneData)
    if (toneData.length === 0) {
        const errorDiv = document.getElementById('post_tone');
        const errorMessage = document.createTextNode("No tone detected!");
        errorDiv.append(errorMessage);
    } else {
        showToneData(toneData);
    }
});


