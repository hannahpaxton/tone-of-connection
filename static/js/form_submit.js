"use strict";

// function submitValidForms () {

    const postForm = document.getElementById('postform');
    const post = document.getElementById("postfield");
    const zip = document.querySelector('input[name="zipcode"]');

    postForm.addEventListener('submit', (evt) => {
        let postShouldSubmit = false
        let zipShouldSubmit = false
        
        // NOT accurately assessing post value
        if (post.value === null) {
          postShouldSubmit = false
        } else {
          postShouldSubmit = true
        }
        
        // accurately assessing zip value
        if (zip.value.length !== 5) {
          zipShouldSubmit = false
        } else {
          zipShouldSubmit = true
        }
        
        // preventing the zip if it's not 5 digits long
        if (zipShouldSubmit && postShouldSubmit) {
            postForm.onsubmit()
        } else if (zipShouldSubmit && !postShouldSubmit)  {
            alert("Write something! Enter a valid post.")
            evt.preventDefault();
        } else if (!zipShouldSubmit && postShouldSubmit) {
            alert("Enter a valid ZIP code");
            evt.preventDefault(); 
        } else {
            alert("Valid ZIP AND post text");
            evt.preventDefault();
        }
    })




    // zipForm.addEventListener('submit', (evt) => {

    //     // Need a way to validate ZIP code
    //     if (zip.length !== 5) {
    //         alert("Valid ZIP Code needed for submission");
    //         evt.preventDefault();
    //     } else {
    //         zipForm.submit();
    //     }
    // });


