# TANKS

![TANKS](./media/mid_tank.png)


Networked tank game using the pygame and twisted python libraries.

To start a game, first make sure the 'SERVER' variable in tank_gs.py is set to the address of the computer the first
player will be using. Whoever will be hosting the game then runs 'python main_server.py' and once the game window
appears the other player can run 'python main_client.py' from their computer to begin the game. The server player
controls the tank on the left side and the client player controls the tank on the right side. Each tank has a health bar
that indicates their remaining health (out of 1000). To move, you press the 'a' and 'd' buttons to move left and right
respectively. To fire missile, you aim your mouse at the angle you wish to fire and left-click to fire. When missiles
hit the opposing tank, they inflict 50 damage. When missiles hit the ground, they destroy a large chunk that is now
traversable (Try digging a tunnel). Wind and gravity both affect the trajectory of the missiles and there is a wind
indicator arrow in the upper right hand corner. When a player loses all of their health, the game will end and each
player's screen will display whether they won or lost, as well as a prompt to press 'q' to quit.
