
import math
import random
import time
import ipdb
from abc import ABC, abstractmethod


class TreeNode:
    def __init__(self, state, parent, action=None):
        """
        :type state: GameState
        :type parent: TreeNode | None
        """
        self.action = action
        self.state = state
        self.isTerminal = state.is_terminal()
        self.isFullyExpanded = self.isTerminal
        self.parent = parent
        self.numVisits = 0
        self.totalReward = 0
        self.children = {}

    def __repr__(self) -> str:
        return "TreeNode({}, {})".format(self.state, self.action)


class MCTS:
    def __init__(self, time_limit=None, iteration_limit=None, exploration_constant=1 / math.sqrt(2)):
        if time_limit is not None:
            if iteration_limit is not None:
                raise ValueError("Cannot have both a time limit and an iteration limit")
            # time taken for each MCTS search in milliseconds
            self.timeLimit = time_limit
            self.limitType = 'time'
        else:
            if iteration_limit is None:
                raise ValueError("Must have either a time limit or an iteration limit")
            # number of iterations of the search
            if iteration_limit < 1:
                raise ValueError("Iteration limit must be greater than one")
            self.searchLimit = iteration_limit
            self.limitType = 'iterations'
        self.explorationConstant = exploration_constant
        self.root = None
        self.global_best_reward = 0

    def search(self, initial_state):
        """
        :type initial_state: GameState
        """
        # short-circuit MCTS when there is only one possible action
        #print("Search Started")
        actions = initial_state.get_possible_actions()
        #print("1")
        if len(actions) == 1:
            return actions[0]

        self.root = TreeNode(initial_state, None)

        start_time = time.time()
        #print("2")
        rounds = 0
        if self.limitType == 'time':
            #print("3")
            time_limit = time.time() + self.timeLimit / 1000
            while time.time() < time_limit:
                self.execute_round()
                rounds += 1
        else:
            #print("4")
            for i in range(self.searchLimit):
                self.execute_round()
                rounds += 1

        time_taken = time.time() - start_time
        #logger.debug('MCTS.search executed {} rounds in {:.2f} sec.'.format(rounds, time_taken))

        best_child = self.get_best_child(self.root, 0)
        #print("5")
        return best_child.action

    def execute_round(self):
        #print("Round Start")
        node = self.select_node(self.root)
        reward = self.rollout(node.state)
        self.backpropagate(node, reward)
        #print("Round End")

    def select_node(self, node):
        """
        :type node: TreeNode
        """
        while not node.isTerminal:
            if node.isFullyExpanded:
                node = self.get_best_child(node, self.explorationConstant)
            else:
                return self.expand(node)
        return node

    def rollout(self, state):
        """
        :type state: GameState
        """
        action_counts = {}
        while not state.is_terminal():
            try:
                action = random.choice(state.get_possible_actions())
            except IndexError:
                raise Exception("Non-terminal state has no possible actions: " + str(state))
            state = state.take_action(action)
            action_counts[str(action)] = action_counts.get(str(action), 0) + 1
            if len(action_counts)>30:
                break
        reward = state.get_reward()
        if reward > self.global_best_reward:
            #logger.info(
            #    'Found new global best reward: {}, action_counts: {}'.format(reward, sorted(action_counts.items())))
            #logger.debug(repr(state))
            self.global_best_reward = reward
        return reward

    @staticmethod
    def expand(node):
        """
        :type node: TreeNode
        """
        actions = node.state.get_possible_actions()
        random.shuffle(actions)
        for action in actions:
            if action not in node.children.keys():
                new_node = TreeNode(node.state.take_action(action), node, action)
                node.children[action] = new_node
                if len(actions) == len(node.children):
                    node.isFullyExpanded = True
                return new_node

        raise Exception("Should never reach here")

    @staticmethod
    def backpropagate(node, reward):
        while node is not None:
            node.numVisits += 1
            node.totalReward += reward
            node = node.parent

    @staticmethod
    def get_best_child(node, exploration_value):
        node_values = [(MCTS.get_node_value(child, node, exploration_value), child) for child in node.children.values()]
        #ipdb.set_trace()
        node_values.sort(key=lambda n: n[0], reverse=True)
        node_values = list(filter(lambda n: n[0] == node_values[0][0], node_values))
        return random.choice(node_values)[1]

    @staticmethod
    def get_node_value(child, node, exploration_value):
        return child.totalReward / child.numVisits + exploration_value * math.sqrt(
            2 * math.log(node.numVisits) / child.numVisits)
            
class GameState(ABC):
    
    #returns true if the game state is terminal, aka that is no additional moves exist, or the game has ended
    @abstractmethod
    def is_terminal(self):
        pass
        
    #returns a list of possible actions
    @abstractmethod
    def get_possible_actions(self):
        pass
        
    #creates a new state, and advances the state by the listed action
    @abstractmethod
    def take_action(self,action):
        pass
        
    #returns the reward of the state, only needed for terminal states
    def get_reward(self):
        pass