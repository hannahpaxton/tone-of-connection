"use strict";

var i = 0;
var defaultCopy = `${postPrompt}`;
var speed = 50;

function typingAnimation() {
    if (i < defaultCopy.length) {
        document.getElementById("typing").innerHTML += defaultCopy.charAt(i);
        i++;
        setTimeout(typingAnimation, speed);
    }
}

typingAnimation();