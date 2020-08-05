document.addEventListener('DOMContentLoaded', function () {

    // Retrieve selector of comment element
    const comment_id = document.querySelector("#comment-text");

    document.querySelector("#submit").addEventListener("click", function (event) {
        addComment(comment_id.dataset.profileId);
        event.preventDefault();
    });

    console.log("DOM content loaded");
});

// Add comment to artist profile
function addComment(profile_id) {
    // Get values from comment field
    const comment_txt = document.querySelector("#comment-text").value;
    const rating_txt = document.querySelector("#rating").value;
    const data = { comment: comment_txt, rating: rating_txt };
    const token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

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
            // Add comment to artist profile page
            let node = document.createElement("P");
            let textnode = document.createTextNode(data.comment);
            node.appendChild(textnode);
            document.querySelector("#comment-box").appendChild(node);
            // Add rating to artist profile page
            let node1 = document.createElement("P");
            let textnode1 = document.createTextNode(data.rating);
            node.appendChild(textnode1);
            document.querySelector("#comment-box").appendChild(node1);
        });
}// End addComment