# TANKS

**By Benedict Becker & Thomas Franceschi**

![TANKS](./media/mid_tank.png)



##Networked tank game using the pygame and twisted python libraries.

### Instructions
To start a game, first make sure the 'SERVER' variable in tank_gs.py is set to the address of the computer the first
player will be using. Whoever will be hosting the game then runs 'python main_server.py' and once the game window
appears the other player can run 'python main_client.py' from their computer to begin the game. The server player
controls the tank on the left side and the client player controls the tank on the right side. Each tank has a health bar
that indicates their remaining health (out of 1000). To move, you press the 'a' and 'd' buttons to move left and right
respectively. To fire missile, you aim your mouse at the angle you wish to fire and left-click to fire. When missiles
hit the opposing tank, they inflict 50 damage. When missiles hit the ground, they destroy a large chunk that is now
traversable (Try digging a tunnel). Wind and gravity both affect the trajectory of the missiles and there is a wind
indicator arrow in the upper right hand corner. When a player loses all of their health, the game will end and each
player's screen will display whether they won or lost, as well as a prompt to press 'q' to quit or 'r' to restart
(only the server has the ability to start a new match).

### A Note on Movement
As of right now, the tanks will always be able to move right. Even if there is a wall blocking its path, it will suddenly 
jump to the next highest ground. We left it this way because the highly interactive (destructive) environment would make for
a lot of stuck tanks if we didn't include this movement workaround.

### A Note on Background
We also had created a shifting parallax background to this game, but unfortunately could not speed it up to the point of not slowing
the rest of the game down. While not included in this version, the code can still be found in "background.py"

### Features
* Fast online gameplay
* Cool tank and explosion graphics (from Google Images)
* Randomly generated map, new every time
* Random wind condition to change the gameplay
* Destructive map
* Realistic gravity for bullets
* Health bars
* 8bit music and violent (loud) sound effects 

### Configuration
There are many constants that affect the networking and gameplay, and can be edited in the game/constants.py file

### Requirements
* numpy
* pygame
* twisted