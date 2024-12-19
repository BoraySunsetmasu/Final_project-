//const API_BASE_URL = "http://35.238.154.158:5000"; // Update as needed
const API_BASE_URL = "http://35.238.154.158:5000"

document.getElementById("submit-button").addEventListener("click", submitForm);
document.getElementById("gpt-button").addEventListener("click", gptResponse);
document.getElementById("download-button").addEventListener("click", downloadExcel);

let data = null;

function submitForm() {
    const stockNumber = document.getElementById("stock-number").value.trim();
    const startDate = document.getElementById("start-date").value.trim();
    const endDate = document.getElementById("end-date").value.trim();

    if (stockNumber && startDate && endDate) {
        fetch(`${API_BASE_URL}/api/analyze_data`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ stock: stockNumber, start: startDate, end: endDate }),
        })
            .then(response => response.json())
            .then(result => {
                data = result;
                displayOptions(result.images);
            })
            .catch(error => alert(`Error: ${error.message}`));
    } else {
        alert("請填寫所有欄位！");
    }
}

function displayOptions(images) {
    const buttonFrame = document.getElementById("button-frame");
    buttonFrame.innerHTML = ""; 
    images.forEach((imagePath, index) => {
        const button = document.createElement("button");
        var button_name = ['Closing Prices History', 'KD History', 'MACD History', 'RSI History', '策略分析']
        button.textContent = button_name[index];
        button.addEventListener("click", () => showImageWithAnimation(imagePath));
        buttonFrame.appendChild(button);
    });
}

function showImageWithAnimation(imagePath) {
    const img = document.getElementById("chart-image");

    img.style.opacity = "0";

    setTimeout(() => {
        fetch(`${API_BASE_URL}/api/show_images`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ image_path: imagePath }),
        })
            .then(response => response.blob())
            .then(blob => {
                img.src = URL.createObjectURL(blob);

                img.style.transition = "opacity 0.5s ease-in";
                img.style.opacity = "1";
            })
            .catch(error => alert(`Error: ${error.message}`));
    }, 500); 
}

function gptResponse() {
    const question = document.getElementById("gpt-question").value.trim();
    if (!question || !data) {
        alert("請輸入問題並先執行查詢！");
        return;
    }
    fetch(`${API_BASE_URL}/api/send_to_gpt`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image_paths: data.images, question }),
    })
        .then(response => response.json())
        .then(result => {
            document.getElementById("gpt-response").value = result.gpt_reply || "AI 顧問無法提供回答";
        })
        .catch(error => alert(`Error: ${error.message}`));
}


function downloadExcel() {
    if (!data) {
        alert("請先執行查詢！");
        return;
    }
    const excelPath = data.excel_path;
    if (excelPath) {
        fetch(`${API_BASE_URL}/api/download_excel?file_path=${excelPath}`)
            .then(response => response.blob())
            .then(blob => {
                const a = document.createElement("a");
                a.href = URL.createObjectURL(blob);
                a.download = "analysis_report.xlsx";
                a.click();
            })
            .catch(error => alert(`Error: ${error.message}`));
    } else {
        alert("無法下載文件！");
    }
}
