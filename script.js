// // Mock hospital data
// const hospitalData = {
//   fever: {
//     specialist: "General Physician",
//     hospitals: [
//       { name: "City Hospital", details: "2 km away, OP available" },
//       { name: "Green Care Clinic", details: "3 km away, OP available" },
//       { name: "Health Plus Center", details: "5 km away, OP available" },
//     ]
//   },
//   cough: {
//     specialist: "Pulmonologist",
//     hospitals: [
//       { name: "Lung Care Hospital", details: "3 km away, OP available" },
//       { name: "Respira Clinic", details: "6 km away, OP available" },
//     ]
//   },
//   headache: {
//     specialist: "Neurologist",
//     hospitals: [
//       { name: "Neuro Center", details: "2.5 km away" },
//       { name: "Brain Health Hospital", details: "5 km away" },
//     ]
//   }
// };

// const steps = document.querySelectorAll(".step-form");
// const stepNumbers = document.querySelectorAll(".progressbar .step");

// let selectedDoctor = "";
// let selectedSpecialist = "";
// let opAmount = 0;

// // Step 1
// document.getElementById("step-1").addEventListener("submit", function (e) {
//   e.preventDefault();

//   const disease = document.getElementById("disease").value.toLowerCase().trim();
//   const specialistDisplay = document.querySelector(".specialist-display");
//   const doctorsList = document.getElementById("doctors-list");

//   doctorsList.innerHTML = "";

//   if (hospitalData[disease]) {
//     const { specialist, hospitals } = hospitalData[disease];
//     selectedSpecialist = specialist;

//     specialistDisplay.textContent = `Specialist: ${specialist}`;

//     hospitals.forEach(h => {
//       const amount = Math.floor(Math.random() * 101) + 450;

//       const card = document.createElement("div");
//       card.className = "card";

//       card.innerHTML = `
//         <div class="card-info">
//           <h3>${h.name}</h3>
//           <p>${h.details}</p>
//           <p>OP Fee: ₹${amount}</p>
//         </div>
//         <div class="card-select">
//           <button type="button" class="select-doctor-btn" data-amount="${amount}">
//             Select
//           </button>
//         </div>
//       `;

//       doctorsList.appendChild(card);
//     });

//     goToStep(1);
//   } else {
//     specialistDisplay.textContent = "No data found for this symptom.";
//   }
// });

// // Step 2
// document.getElementById("doctors-list").addEventListener("click", function (e) {
//   if (e.target.classList.contains("select-doctor-btn")) {

//     selectedDoctor = e.target.closest(".card").querySelector("h3").textContent;
//     opAmount = e.target.dataset.amount;

//     // Enable button
//     document.getElementById("to-step-3").disabled = false;

//     // Highlight selected
//     document.querySelectorAll(".card").forEach(card => card.classList.remove("selected"));
//     e.target.closest(".card").classList.add("selected");
//   }
// });

// // Navigation
// document.getElementById("to-step-3").addEventListener("click", () => {
//   // ✅ Set values WHEN entering step 3
//   document.getElementById("display-doctor").textContent = selectedDoctor;
//   document.getElementById("display-specialist").textContent = selectedSpecialist;
//   document.getElementById("display-amount").textContent = opAmount;

//   goToStep(2);
// });

// document.getElementById("back-to-step-1").addEventListener("click", () => goToStep(0));
// document.getElementById("back-to-step-2").addEventListener("click", () => goToStep(1));

// // Reset
// document.getElementById("new-booking").addEventListener("click", () => {
//   goToStep(0);

//   document.getElementById("step-1").reset();
//   document.querySelector(".specialist-display").textContent = "";
//   document.getElementById("doctors-list").innerHTML = "";
//   document.getElementById("to-step-3").disabled = true;
// });

// // Step 3 → Confirm Booking
// document.getElementById("step-3").addEventListener("submit", function (e) {
//   e.preventDefault();

//   const opId = "OP" + Math.floor(Math.random() * 1000000);

//   document.getElementById("op-id").textContent = opId;
//   document.getElementById("final-doctor").textContent = selectedDoctor;
//   document.getElementById("final-specialist").textContent = selectedSpecialist;
//   document.getElementById("final-amount").textContent = opAmount;

//   goToStep(3);
// });

// // Step navigation
// function goToStep(stepIndex) {
//   steps.forEach((s, i) => s.classList.toggle("active", i === stepIndex));
//   stepNumbers.forEach((s, i) => s.classList.toggle("active", i <= stepIndex));
// }