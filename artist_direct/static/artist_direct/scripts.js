document.addEventListener('DOMContentLoaded', function () {

    // Retrieve profile_id of user
    const comment_id = document.querySelector("#comment-text");
 
    document.querySelector("#submit").addEventListener("click", function () {
        
        addComment(comment_id.dataset.profileId);
        console.log("This is after function call.")      
        return false;
    });

    console.log("DOM content loaded");
});

// Add comment to artist profile
function addComment(profile_id) {
    // Get value from comment field
    const comment_txt = document.querySelector("#comment-text").value;
    const rating_txt = document.querySelector("#rating").value;
    const data = {comment:comment_txt, rating:rating_txt};

    const token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    console.log(profile_id);

    fetch(`/add_comment/${profile_id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": token
        },
        body: JSON.stringify(data),
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            
            let node = document.createElement("P");
            let textnode = document.createTextNode(data.comment);
            node.appendChild(textnode);
            document.querySelector("#comment-box").appendChild(node);
            //document.querySelector("#comment-box").appendChild(document.createTextNode(data.comment));
            //document.querySelector("#rating-box").appendChild(document.createTextNode(data.stars));
        });
}// End addComment