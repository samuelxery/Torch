async function send() {
    let value = document.getElementById("num").value;

    let res = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ number: Number(value) })
    });

    let data = await res.json();
    document.getElementById("output").innerText = "result: " + data.result;
}