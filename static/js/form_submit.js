"use strict";

// function submitValidForms () {

    const postForm = document.getElementById('postform');
    const post = document.getElementById("postfield");
    const zip = document.querySelector('input[name="zipcode"]');

    postForm.addEventListener('submit', (evt) => {
        let postShouldSubmit = false
        let zipShouldSubmit = false
        
        if (!post.value) {
          postShouldSubmit = false
        } else {
          postShouldSubmit = true
        }
        console.log(post)
        
        if (zip.length !== 5) {
          zipShouldSubmit = false
        } else {
          zipShouldSubmit = true
        }
        console.log(zip)
        
        console.log(zip.length);
        if (zipShouldSubmit && postShouldSubmit) {
            postForm.onsubmit()
        } else if (zipShouldSubmit && !postShouldSubmit)  {
            alert("Write something! Enter a valid post.")
        } else if (!zipShouldSubmit && postShouldSubmit) {
            alert("Enter a valid ZIP code") 
        } else {
            alert("Valid ZIP AND post text")
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


