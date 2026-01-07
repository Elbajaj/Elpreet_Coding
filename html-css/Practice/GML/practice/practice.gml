//player movement and gravity const (create)
move_spd = 4;
jump_spd = 7;
grav = 0.3;

xspd = 0;
yspd = 0;

image_xscale = 1;

//defining keybinds (step)
var move = keyboard_check(ord("D")) - keyboard_check(ord("A"));

//flips the player left and right depending if they pressed "A" "D"
if (move != 0) {
    image_xscale = sign(move);
}

//define the speed of movement
xspd = move * move_spd;

//gravity
yspd += grav;

//jumping
if (keyboard_check_pressed(vk_space)) {
    yspd = -jump_spd;
}

//the way to add left and right movement with x/y speed
x += xspd;
y += yspd;

//tilemap collisions
if (yspd != 0 or xspd != 0) {
    move_and_collide(yspd * move_spd, xspd * move_spd, tile_map, true);
}

//collisions checks
if place_meeting(x, y, obj_anything) {
    //any command to execute
}

//constucters
function Player(_name, _hp) {
    return {
        // Properties
        name: _name,
        hp: _hp,
        score: 0,

        // Way to take damage
        take_damage: function(amount) {
            self.hp = max(0, self.hp - amount);
            if (self.hp <= 0) {
                show_debug_message(self.name + " has been defeated!");
            }
        },

        // Way to add score
        add_score: function(points) {
            self.score += points;
        }
    };
}

// Example usage:
var p1 = obj_player("Name", 100);
p1.add_score(50);
p1.take_damage(30);

show_debug_message(p1.name + " has " + string(p1.hp) + " HP and " + string(p1.score) + " points.");