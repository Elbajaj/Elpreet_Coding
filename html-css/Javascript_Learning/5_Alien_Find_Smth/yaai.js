let alien = document.getElementById("alien");
let star = document.getElementById("star");
let scoreDisplay = document.getElementById("score");

let posX = 270;
let posY = 170;
const step = 10;
let score = 0;

// Keyboard control
document.addEventListener("keydown", function (event) {
    if (event.key === "ArrowRight") posX += step;
    else if (event.key === "ArrowLeft") posX -= step;
    else if (event.key === "ArrowUp") posY -= step;
    else if (event.key === "ArrowDown") posY += step;

    // Keep inside game area
    posX = Math.max(0, Math.min(posX, 540));
    posY = Math.max(0, Math.min(posY, 340));

    // Move alien
    alien.style.left = posX + "px";
    alien.style.top = posY + "px";

    // Check for collision
    if (isTouching(alien, star)) {
        score++;
        scoreDisplay.textContent = score;

        // Move star to new random position
        let newX = Math.floor(Math.random() * 550);
        let newY = Math.floor(Math.random() * 350);
        star.style.left = newX + "px";
        star.style.top = newY + "px";
    }
});

// Simple collision detection
function isTouching(a, b) {
    let aRect = a.getBoundingClientRect();
    let bRect = b.getBoundingClientRect();

    return !(
        aRect.top > bRect.bottom ||
        aRect.bottom < bRect.top ||
        aRect.right < bRect.left ||
        aRect.left > bRect.right
    );
}