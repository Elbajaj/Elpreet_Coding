let alienFirstNames = ["Globglogabgalab", "Blorptar", "Xarnax", "Wibbly", "Glorm"]
let alienHomePlanets = ["Xylotron-9", "Glorpaxia", "Zarnok-3", "Nebulon Prime", "Vortexia"]
let alienOgSpecies = ["Dame Tu Costia", "Alien", "Plastic", "Latex Man", "SHINNYY"]

function clearAlien() {
    let output = "Click the button to meet a new Alien Guy!";
    document.getElementById("alienOutput").textContent = output;
}
function generateAlien() {
    let randomName = alienFirstNames[Math.floor(Math.random() * alienFirstNames.length)];
    let randomPlanet = alienHomePlanets[Math.floor(Math.random() * alienHomePlanets.length)];
    let randomSpecie = alienOgSpecies[Math.floor(Math.random() * alienOgSpecies.length)];

    let output = randomName + " from " + randomPlanet + " is a " + randomSpecie + " and says hi!";
    document.getElementById("alienOutput").textContent = output;

}