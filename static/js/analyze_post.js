"use strict";

function showToneData (toneData) {
    for (const data of toneData) {
        const newDiv = document.createElement("div");
            const toneQuality = document.createTextNode(data.tone_quality + ", ");
                newDiv.append(toneQuality);
            const toneScore = document.createTextNode(data.tone_score + "%");
                newDiv.append(toneScore);
            const hexValue = document.createElement("div")
                hexValue.style.backgroundColor=data.hex_value;
                hexValue.style.height="20px"; 
                hexValue.style.width="20px";
                newDiv.append(hexValue);
        const currentDiv = document.getElementById('post_tone');
        currentDiv.appendChild(newDiv);
    }    
}

const toneAnalysis = `/api/tone/${postID}`; 

fetch(toneAnalysis)
.then((response) => response.json())
.then((toneData) => {
    showToneData(toneData)
});


