document.getElementById("predictionForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    const students = parseFloat(document.getElementById("students").value);
    const attendance = parseFloat(document.getElementById("attendance").value);
    const previousConsumption = parseFloat(
        document.getElementById("previousConsumption").value
    );

    if (attendance > students) {
        alert("Expected attendance cannot be greater than total students.");
        return;
    }

    const data = {
        Students: students,
        Attendance: attendance,
        Meal_Type: document.getElementById("mealType").value,
        Menu: document.getElementById("menu").value,
        Weather: document.getElementById("weather").value,
        Special_Event: document.getElementById("specialEvent").value,
        Holiday: document.getElementById("holiday").value,
        Previous_Consumption_kg: previousConsumption
    };

    try {
        const response = await fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Prediction failed.");
        }

        document.getElementById("predictedConsumption").textContent =
            result.predicted_consumption_kg.toFixed(2) + " kg";

        document.getElementById("recommendedQuantity").textContent =
            result.recommended_quantity_kg.toFixed(2) + " kg";

    } catch (error) {
        console.error(error);
        alert("Unable to connect to the prediction server. Make sure Flask is running.");
    }
});
