document.getElementById("uploadForm").addEventListener("submit", async (event) => {
    event.preventDefault();

    const file1 = document.getElementById("file1").files[0];
    const file2 = document.getElementById("file2").files[0];
    
    if (!file1 || !file2) {
        alert("Please upload both images.");
        return;
    }

    const formData = new FormData();
    formData.append("file1", file1);
    formData.append("file2", file2);

    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = "Processing...";

    try {
        const response = await fetch("http://127.0.0.1:8000/verify", {
            method: "POST",
            body: formData
        });

        const result = await response.json();
        if (response.ok) {
            resultDiv.innerHTML = `
                <p><strong>Are they the same person?</strong> ${result.is_same_person ? "Yes" : "No"}</p>
                <p><strong>Similarity Score:</strong> ${result.similarity_score.toFixed(4)}</p>
            `;
        } else {
            resultDiv.innerHTML = `<p style="color: red;">Error: ${result.error}</p>`;
        }
    } catch (error) {
        resultDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    }
});
