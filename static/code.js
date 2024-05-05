const bars = document.querySelector("#bars");
const colorBars = document.querySelector(".color-bars");
const strengthDiv = document.querySelector("#strength");
const passwordInput = document.querySelector("#password");
const checkPwBtn = document.getElementById("check-pass");
const dropdownModel = document.getElementById("dropdown-model");

const strength = {
  1: "very weak",
  2: "weak",
  3: "average",
  4: "strong",
  5: "very strong",
};

const strengthColor = {
  1: "#FF0000",
  2: "#FF4500",
  3: "#FFD700",
  4: "#32CD32",
  5: "#0000FF",
};

function checkStrength(num) {
  let strengthIndicator = 0;
  if (num < 1) {
    if (num < 0.2) {
      strengthIndicator = 1;
    } else if (0.2 <= num && num < 0.4) {
      strengthIndicator = 2;
    } else if (0.4 <= num && num < 0.6) {
      strengthIndicator = 3;
    } else if (0.6 <= num && num < 0.8) {
      strengthIndicator = 4;
    } else {
      strengthIndicator = 5;
    }
  } else {
    strengthIndicator = num;
  }
  return strengthIndicator;
}

checkPwBtn.addEventListener("click", () => {
  let password = passwordInput.value;
  let model = dropdownModel.value;
  if (model == "default") {
    alert("Please select a model!");
    return;
  }
  const formData = new FormData();
  formData.append("password", password);
  formData.append("model", model);
  let passwordStrengthData;

  // Fetch the data
  fetch("/strength", {
    method: "POST",
    body: formData,
  })
    .then((res) => res.json())
    .then((data) => {
      passwordStrengthData = data;
      handlePasswordStrength(passwordStrengthData);
    })
    .catch((error) => {
      console.log(error);
    });
});

function handlePasswordStrength(data) {
  console.clear();
  console.log("[debug] received data from api, we are checking...");
  console.log("[debug] isClassification:", data.isClassification);
  console.log("[debug] model:", data.model);
  console.log("[debug] strength:", data.strength);

  let strengthIndicator = checkStrength(parseFloat(data.strength));
  let strengthText = strength[strengthIndicator]
    ? strength[strengthIndicator]
    : "very weak";
  console.log("[debug] after parsed:", strengthIndicator);

  if (data.isClassification) {
    bars.style.width = "100%";
    bars.style.background = "rgba(255, 255, 255, 0.1)";
    colorBars.style.width = `${strengthIndicator * 20}%`;
    colorBars.style.background = strengthColor[strengthIndicator];
    strengthDiv.innerText = `Your password is ${strengthText}.`;
  } else {
    bars.style.width = "100%";
    bars.style.background = "rgba(255, 255, 255, 0.1)";
    colorBars.style.width = `${data.strength * 100}%`;
    colorBars.style.background = strengthColor[strengthIndicator];
    strengthDiv.innerText = `Your password is ${strengthText}.`;
  }
}
