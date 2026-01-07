function talkToHuman() {
    // Ask the user their name
    let humanName = prompt("Greetings, Earthling! What is your name?");

    // Check if they typed something
    if (humanName) {
        // Compose a message
        let message = "👾 Hello, " + humanName + "! I am Zorgo from Xylotron-9. We come in peace.";

        // Show message on page
        document.getElementById("greetingOutput").textContent = message;
    } else {
        // If they cancel or leave blank
        document.getElementById("greetingOutput").textContent = "No name? Mysterious Earthling...";
    }
}