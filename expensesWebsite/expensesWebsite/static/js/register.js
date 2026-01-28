const usernameField = document.querySelector("#usernameField");
const usernameFeedbackField = document.querySelector(
  ".invalid-feedback-username",
);
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput");

const emailField = document.querySelector("#emailField");
const emailFeedbackField = document.querySelector(".invalid-feedback-email");


usernameField.addEventListener("keyup", (e) => {
  console.log("Key up event detected");
  const usernameVal = e.target.value;
  usernameSuccessOutput.textContent = `Checking ${usernameVal}...`;
  usernameSuccessOutput.style.display = "block";

  usernameFeedbackField.style.display = "none";
  usernameField.classList.remove("is-invalid");

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
        }
      });
  }
});

emailField.addEventListener("keyup", (e) => {
  console.log("Key up event detected");
  const emailVal = e.target.value;

  emailFeedbackField.style.display = "none";
  emailField.classList.remove("is-invalid");
  

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
        }
      });
  }
});
