"use strict";

var i = 0;
var copy = "This is Tone of Connection - an anonymous journal that analyzes your mood and translates it to color";
var speed = 50;

function typingAnimation() {
    if (i < copy.length) {
        document.getElementById("typing").innerHTML += copy.charAt(i);
        i++;
        setTimeout(typingAnimation, speed);
    }
}

typingAnimation();