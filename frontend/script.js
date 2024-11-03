document.getElementById("register-btn").addEventListener("click", async () => {
    const username = document.getElementById("reg-username").value;
    const password = document.getElementById("reg-password").value;

    const response = await fetch("http://localhost:5001/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
    });
    const data = await response.json();
    alert(data.message);
});

document.getElementById("login-btn").addEventListener("click", async () => {
    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;

    const response = await fetch("http://localhost:5001/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
    });
    const data = await response.json();
    alert(data.message);
    if (response.ok) {
        document.getElementById("auth").style.display = "none";
        document.getElementById("post-section").style.display = "block";
        loadPosts();
    }
});

document.getElementById("post-btn").addEventListener("click", async () => {
    const imageInput = document.getElementById("image-input");
    const caption = document.getElementById("caption-input").value;

    const formData = new FormData();
    formData.append("image", imageInput.files[0]);
    formData.append("caption", caption);

    const response = await fetch("http://localhost:5003/posts", {
        method: "POST",
        body: formData,
    });
    const data = await response.json();
    alert(data.message);
    if (response.ok) {
        loadPosts();
        document.getElementById("caption-input").value = '';
        imageInput.value = '';
    }
});

async function loadPosts() {
    const response = await fetch("http://localhost:5003/posts");
    const posts = await response.json();
    const postList = document.getElementById("post-list");
    postList.innerHTML = '';
    posts.forEach((post) => {
        const postDiv = document.createElement("div");
        postDiv.innerHTML = `<img src="${post.image_path}" alt="Post" style="width:100%;"><p>${post.caption}</p>`;
        postList.appendChild(postDiv);
    });
}
