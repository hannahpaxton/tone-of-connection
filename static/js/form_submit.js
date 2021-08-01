"use strict";

    const postForm = document.getElementById('postform');
    const post = document.getElementById("postfield");
    const zip = document.querySelector('input[name="zipcode"]');

    postForm.addEventListener('submit', async (evt) => {
        evt.preventDefault();
        let postShouldSubmit = false
        let zipShouldSubmit = false
        
        if (post.value === "") {
          postShouldSubmit = false
        } else {
          postShouldSubmit = true
        };

        if (zip.value.length === 5) {
          const response = await fetch('/geocode?zipcode='+ encodeURIComponent(zip.value)) 
            if (response.status === 500){
              alert("Where are you at again? Enter a valid 5 digit ZIP code");
            }
          const data = await response.json()
          if (Array.isArray(data.results)) {
            zipShouldSubmit = true
          } else {
            zipShouldSubmit = false
          }
        }

        if (zipShouldSubmit && postShouldSubmit) {
          postForm.submit()
        } else if (zipShouldSubmit && !postShouldSubmit)  {
          alert("Write something! Enter a post.")
        } else if (!zipShouldSubmit && postShouldSubmit) {
          alert("Where are you at again? Enter a valid 5 digit ZIP code");
        } else {
          alert("Sorry! Enter a valid 5 digit ZIP code and a post");
        } 
        
    });








