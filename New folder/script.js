async function generateSummary() {

    const fileInput = document.getElementById("fileInput");
    const summary = document.getElementById("summary");
    const solveButton = document.getElementById("solveButton");
    const clearButton = document.getElementById("clearButton");
    const loading = document.getElementById("loading");

    if (fileInput.files.length === 0) {

        summary.innerText =
            "❌ Please upload a question first.";

        return;
    }

    const file = fileInput.files[0];

    const allowedTypes = [
        "image/jpeg",
        "image/png",
        "image/webp",
        "image/gif",
        "application/pdf"
    ];

    if (!allowedTypes.includes(file.type)) {

        summary.innerText =
            "❌ Please upload a JPG, PNG, WEBP, GIF image or PDF.";

        return;
    }


    // Disable buttons while AI is working
    solveButton.disabled = true;
    clearButton.disabled = true;

    // Show loading animation
    loading.style.display = "block";

    summary.innerText =
        "🤖 AI is reading your question...\n\nPlease wait.";


    try {

        const formData = new FormData();

        formData.append("file", file);


        const response = await fetch(
            "https://smartstudy-ai-1-fj1s.onrender.com/solve",
            {
                method: "POST",
                body: formData
            }
        );


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.error || "Server error"
            );

        }


        const answer = data.summary || "";


        summary.innerText =
            "🤖 AI Solution\n\n" + answer;


    }

    catch (error) {

        console.error(error);

        summary.innerText =
            "❌ Unable to generate the answer.\n\n" +
            error.message;

    }

    finally {

        // Hide loading animation
        loading.style.display = "none";

        // Enable buttons again
        solveButton.disabled = false;
        clearButton.disabled = false;

    }

}


/* SHOW SELECTED FILE NAME */

function showFileName() {

    const fileInput = document.getElementById("fileInput");
    const fileName = document.getElementById("fileName");


    if (fileInput.files.length === 0) {

        fileName.innerText =
            "No file selected";

        return;

    }


    fileName.innerText =
        "📎 Selected: " + fileInput.files[0].name;

}


/* CLEAR EVERYTHING */

function clearAll() {

    const fileInput = document.getElementById("fileInput");
    const fileName = document.getElementById("fileName");
    const summary = document.getElementById("summary");
    const loading = document.getElementById("loading");

    fileInput.value = "";

    fileName.innerText =
        "No file selected";

    summary.innerText =
        'Upload a question and click "Solve Question".';

    loading.style.display = "none";

}