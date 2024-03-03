import random
from typing import Dict
import numpy as np

class Action:
    Nothing = 0
    Button1 = 1
    Button2 = 2

class Environment:
    def __init__(self, mean = None, vel = None):
        self.mean = random.random() - .5 if mean is None else mean
        self.vel = (random.random() - .5) / 5 if vel is None else vel

    def copy(self):
        return Environment(self.mean, self.vel)

    def play(self, action: int):
        if action == Action.Button1:
            self.mean += self.vel
        elif action == Action.Button2:
            self.mean -= self.vel

        rndVal = np.random.normal(self.mean, 1)
        value = 0 if rndVal < 0 else 1
        return value

class RandomAgent:
    name = "RandomAgent"

    def act(self, _):
        return random.choice([Action.Nothing, Action.Button1, Action.Button2])

    def reset(self):
        pass

# This agent tries 1 action for 10 turns then the other for 10 turns. Which ever one gave the highest amount of 1s he presses for the most
class SmartAgent:
    name = "SmartAgent"

    def __init__(self):
        self.reset()

    def reset(self):
        self.phase = "Press1"
        self.count = 0
        self.action1Wins = 0
        self.action2Wins = 0

    def act(self, observation):
        self.count += 1

        if self.phase == "Press1":
            self.action1Wins += observation
            if self.count == 100:
                self.count = 0
                self.phase = "Obs1"
            return Action.Button1

        elif self.phase == "Obs1":
            self.action1Wins += observation
            if self.count == 100:
                self.count = 0
                self.phase = "Press2"
            return Action.Nothing

        elif self.phase == "Press2":
            self.action2Wins += observation
            if self.count == 100:
                self.count = 0
                self.phase = "Obs2"
            return Action.Button2

        elif self.phase == "Obs2":
            self.action2Wins += observation
            if self.count == 100:
                self.count = 0
                self.phase = "Exploit"
            return Action.Nothing

        else:
            if self.action1Wins > self.action2Wins:
                return Action.Button1
            else:
                return Action.Button2

class Arena: 
    agent_scores: Dict[str, int] = {}

    def __init__(self, agents):
        self.agents = agents
        for agent in agents:
            self.agent_scores[agent.name] = 0
        self.episodes = 100
        self.iterations = 5000

    def play_in_env(self, env: Environment, agent):
        obs = 0
        for _ in range(self.iterations):
            action = agent.act(obs)
            obs = env.play(action)
        agent.reset()

    def run(self):
        for _ in range(self.episodes):
            env = Environment()
            scores: Dict[str, float] = {}
            for agent in self.agents:
                copy_env = env.copy()
                self.play_in_env(copy_env, agent)
                scores[agent.name] = copy_env.mean

            best_agent = max(scores, key=scores.get)
            self.agent_scores[best_agent] += 1

        for agent in self.agents:
            print(agent.name, self.agent_scores[agent.name])

agent1 = RandomAgent()
agent2 = SmartAgent()
arena = Arena([agent1, agent2])
arena.run()

