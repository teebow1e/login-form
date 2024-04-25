const bars = document.querySelector("#bars");
const strengthDiv = document.querySelector("#strength");
const passwordInput = document.querySelector("#password");
const checkPwBtn = document.getElementById("check-pass");
const dropdownModel = document.getElementById("dropdown-model");

const strength = {
  1: "Super Weak",
  2: "Weak",
  3: "Medium",
  4: "Strong",
  5: "Very Strong",
};

function checkStrength(num){
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
  const formData = new FormData();
  formData.append("password", password);
  formData.append("model", model);
  fetch("/strength", {
    method: "POST",
    body: formData,
  })
    .then((res) => res.json())
    .then((data) => {
      console.log("Received from API: ", data);
      let strengthIndicator = checkStrength(parseFloat(data));
      let strengthText = strength[strengthIndicator];
      console.log("After parsed: ", strengthIndicator)
      
      if (strengthText) {
        strengthDiv.innerText = `${strengthText} Password`;
        bars.className = "";
        bars.classList.add(`strength-${strengthIndicator}`);
      } else {
        strengthDiv.innerText = "Your password is too weak!";
      }
    }).catch((error) => {
      console.log(error);
    });
});