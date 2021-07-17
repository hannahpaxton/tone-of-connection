"use strict";

    const postForm = document.getElementById('postform');
    const post = document.getElementById("postfield");
    const zip = document.querySelector('input[name="zipcode"]');

    postForm.addEventListener('submit', (evt) => {
        let postShouldSubmit = false
        let zipShouldSubmit = false
        
        if (post.value === "") {
          postShouldSubmit = false
        } else {
          postShouldSubmit = true
        }
   
        // accurately assessing zip value, need to check for correct zip, not just 5 digits
        if (zip.value.length !== 5) {
          zipShouldSubmit = false
        } else {
          zipShouldSubmit = true
        }
        
        // preventing the zip if it's not 5 digits long
        if (zipShouldSubmit && postShouldSubmit) {
            postForm.submit()
        } else if (zipShouldSubmit && !postShouldSubmit)  {
            alert("Write something! Enter a valid post.")
            evt.preventDefault();
        } else if (!zipShouldSubmit && postShouldSubmit) {
            alert("Where are you at again? Enter a valid ZIP code");
            evt.preventDefault(); 
        } else {
            alert("Sorry! Enter a valid ZIP code and valid post");
            evt.preventDefault();
        }
    })






