function halloAlien() {
    let status = document.getElementById("noooorText");
    let alien = document.getElementById("noooorImg");

    status.textContext = "Opening the nOoOoOrRrR... stand back!!"

    setTimeout(function () {
        alien.classList.add("opening")
        alien.style.display = "inline-block";
        status.textContent = "nOoOoOrRrR Man Has Arrived!!";
    }, 2000);
}