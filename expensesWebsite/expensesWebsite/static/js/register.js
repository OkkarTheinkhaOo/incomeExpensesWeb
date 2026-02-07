const usernameField = document.querySelector("#usernameField");
const usernameFeedbackField = document.querySelector(
  ".invalid-feedback-username",
);
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput");

const emailField = document.querySelector("#emailField");
const emailFeedbackField = document.querySelector(".invalid-feedback-email");

const passwordToggle = document.querySelector(".passwordToggle");
const passwordField = document.querySelector("#passwordField");

const submitBtn = document.querySelector(".submit-btn");

const handleToggleInput = (e) => {
  if (passwordToggle.textContent === "SHOW") {
    passwordToggle.textContent = "HIDE";
    passwordField.setAttribute("type", "text");
    
  }else {
    passwordToggle.textContent = "SHOW";
    passwordField.setAttribute("type", "password");
  }
}
passwordToggle.addEventListener("click", handleToggleInput);

usernameField.addEventListener("keyup", (e) => {
  console.log("Key up event detected");
  const usernameVal = e.target.value;
  usernameSuccessOutput.textContent = `Checking ${usernameVal}...`;
  usernameSuccessOutput.style.display = "block";

  usernameFeedbackField.style.display = "none";
  usernameField.classList.remove("is-invalid");

  submitBtn.disabled = false;

  if (usernameVal.length > 0) {
    fetch("/authentication/validate-username", {
      body: JSON.stringify({ username: usernameVal }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data received:", data);
        usernameSuccessOutput.style.display = "none";
        if (data.username_error) {
          usernameField.classList.add("is-invalid");
          usernameFeedbackField.innerHTML = `<p>${data.username_error}</p>`;
          usernameFeedbackField.style.display = "block";
          submitBtn.disabled = true;
        }
      });
  }
});

emailField.addEventListener("keyup", (e) => {
  console.log("Key up event detected");
  const emailVal = e.target.value;

  emailFeedbackField.style.display = "none";
  emailField.classList.remove("is-invalid");
  
  submitBtn.disabled = false;

  if (emailVal.length > 0) {
    fetch("/authentication/validate-email", {
      body: JSON.stringify({ email: emailVal }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data received:", data);      
        if (data.email_error) {
          emailField.classList.add("is-invalid");
          emailFeedbackField.innerHTML = `<p>${data.email_error}</p>`;
          emailFeedbackField.style.display = "block";
          submitBtn.disabled = true;
        }
      });
  }
});

