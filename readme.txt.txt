Welcome to Anime Pong! 

Game Described on a High Level:

This game mimics the classic Atari Pong game. The objective is to score the ball by hitting it so it crosses the opponent's side! You have to defend your goal by moving the pong paddle horizontally. However, there are special twists to the pong game which you will find out when you play!

1. Installing the Game:

In order to run the game, you must first install a few modules:

In the shell, type in pip install "insert module name here"

Replace "filename" with the following module names:
-pygame
-os
-pyaudio
-audioop

2. To run the game, have all the files in the same folder. Then, by using your shell, run the run_game file. 

3. Enjoy the game! 




-----Updates-----
This project has undergone many updates over the past three weeks.

Originally, my project started as a personal voice assistant that would use machine learning libraries. However, that became too difficult and unrealistic, so I decided to move on to coding the game of pong that would have an AI that would use machine learning to eventually become undefeatable. That also became too difficult and unrealistic.

Finally, I decided to resort to making pong game with many improvements and twists from the original Atari retro game. First, I would apply real world physics mechanics to the game. I mimicked accurate collisions between the walls and the ball, and the walls and the paddles. Additionally, I also gave the player the option to rotate his/her own paddle, and when rotated, would also mimic a real-world physics collision when it collides with the ball. 

Additionally, I spent a long amount of time coding my AI's. My hard AI is able to predict the final y-position of the ball once the ball collides with the player's own paddle. This may seem unbeatable, but one of the twists I added is the ability for your player to shoot bullets. The aim is to use these bullets to hit spawning ramen powerups to fill up the user's mana bar. Once the user's mana bar is full, then the player has the ability to use his ultimate weapon!

This ultimate weapon can only be used by screaming into the microphone, since the only way to trigger it is by emitting a volume over a specific threshold frequency. This will release the ultimate weapon, and if it hits the opponent, you win! 

Learning how to use pygame, desinging a UI for the very first time, and applying physics to a game were all huge challenges for me, but they were things I learned to do over the course of the past few weeks. Happy Ponging!!!!