# Snake Game with Deep Q-Network (DQN)
 In this project we aim to make an intelligent agent that can learn to play the classic Snake game using reinforcement learning techniques. The agent uses the powerful Deep Q-Network algorithm, a type of reinforcement learning, to make decisions in the game environment.
 ## Project Components
 ### 1. Snake Game Environment
 The Snake game environment provides a graphical user interface (GUI) that allows the player to interact with the game. The snake moves around a grid, eating food and growing in length. The game ends if the snake collides with any walls or itself. 
 ### 2. Deep Q-Network (DQN) Architecture
 The Deep Q-Network (DQN) acts as the brain of our agent. It takes a list of 11 boolean values as input, representing the game state and outputs Q-values for each possible action in the action space of 3 actions.The DQN is implemented using 3 Dense neural networks and employs techniques such as experience replay.
 ### 3. Reinforcement Learning
 The DQN agent is trained using the Q-learning algorithm with experience replay. It interacts with the game environment, observes states, takes actions, and receives rewards. The DQN updates its parameters based on the rewards and experiences gathered during gameplay, gradually learning optimal strategies for playing the game.
 ## How To Run
 To train the Snake game yourself:
 1. Clone this repository to your local machine.
 2. Install the required dependencies mentioned in the `requirements.txt` file.
 3. Run the `agent.py` script.
 4. It will Display the game running and also output the graph of score and mean_score per game.

## How It Went
1. For first few eps it went randomly .
2. around 20-25 ep it starts to go towards food consistently.
![](https://github.com/deepu718/Snake_AI/blob/main/snake_gif/episode_19_score_2.gif)![](https://github.com/deepu718/Snake_AI/blob/main/snake_gif/episode_26_score_11.gif)
3. around 40 ep it start getting score over 15.
![](https://github.com/deepu718/Snake_AI/blob/main/snake_gif/episode_37_score_19.gif)![](https://github.com/deepu718/Snake_AI/blob/main/snake_gif/episode_38_score_23.gif)
5. Best run was at ep 102 with a score of 29.
![](https://github.com/deepu718/Snake_AI/blob/main/snake_gif/episode_102_score_29.gif)
 
 
 