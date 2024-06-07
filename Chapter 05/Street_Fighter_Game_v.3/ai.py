import py_trees as pt
import py_trees.console as console
import math
import random


def is_attack_mode(ai_controller):
    if ai_controller.health > random.randint(0, 50) or ai_controller.health > ai_controller.opponent_health:
        print("AI is in attack mode.")
        return pt.common.Status.SUCCESS
    else:
        return pt.common.Status.FAILURE

def is_defend_mode(ai_controller):
    if ai_controller.health <= random.randint(0, 50) and ai_controller.health <= ai_controller.opponent_health:
        print("AI is in defend mode.")
        return pt.common.Status.SUCCESS
    else:
        return pt.common.Status.FAILURE

def move_towards(ai_controller):
    if ai_controller.range_to_opponent > ai_controller.attack_range:
        print("AI is moving towards the opponent.")
        ai_controller.state_changes = {
                    "action": "movement",
                    "dx": -ai_controller.direction_to_opponent
                }
        return pt.common.Status.SUCCESS
    else:
        return pt.common.Status.FAILURE

def attack(ai_controller):
    if ai_controller.range_to_opponent <= ai_controller.attack_range:
        print("AI is attacking the opponent.")
        ai_controller.state_changes = {
                        "action": "attacking",
                        "attack_type": random.choice([1, 2])
                        }
        return pt.common.Status.SUCCESS
    else:
        return pt.common.Status.FAILURE

def move_away(ai_controller):
    if ai_controller.health < 25:
        print("AI is moving away from the opponent.")
        ai_controller.state_changes = {
                    "action": "movement",
                    "dx": ai_controller.direction_to_opponent
                }
        return pt.common.Status.SUCCESS
    else:
        return pt.common.Status.FAILURE

def jump(ai_controller):
    if ai_controller.range_to_opponent <= ai_controller.attack_range:
        print("AI is jumping.")
        ai_controller.state_changes = {
            "action": "jumping" 
            }
        return pt.common.Status.SUCCESS
    else:
        return pt.common.Status.FAILURE

class CustomBehaviour(pt.behaviour.Behaviour):
    def __init__(self, name, fn, ai_controller):
        super().__init__(name)
        self.fn = fn
        self.ai_controller = ai_controller

    def update(self):
        return self.fn(self.ai_controller)

class AIController:
    def __init__(self, player):
        self.player = player
        self.state_changes = {}    
        self.create_btree()  
        self.difficulty = 1  

    def get_action(self, game_state):
        self.state_changes = {}
        
        # Extract relevant game state information
        fighter = game_state[f"fighter_{self.player}"]
        opponent = game_state[f"fighter_{3 - self.player}"]
        round_over = game_state["round_over"]
        
        self.health = fighter["health"]
        self.opponent_health = opponent["health"]
        range = fighter["position"].x - opponent["position"].x
        self.range_to_opponent = abs(range)
        self.direction_to_opponent = math.copysign(1, range)
        self.attack_range = 150
        
        print(f"AI State H{self.health}, O{self.opponent_health}, R{self.range_to_opponent}, A{self.attack_range}")
        
        # Implement your AI logic here
        if not round_over:
            if fighter["alive"]:   
                if random.random() < self.difficulty*.1:
                    self.tree.tick()
        
        return self.state_changes
    
    def create_btree(self):
        ai_controller = self

        root = pt.composites.Selector(
            name="AI Behavior",
            memory=False,
            children=[
                pt.composites.Sequence(
                    name="Attack Mode",
                    memory=False,
                    children=[
                        CustomBehaviour("Is Attack Mode", is_attack_mode, ai_controller),
                        pt.composites.Selector(
                            name="Attack Actions",
                            memory=False,
                            children=[
                                CustomBehaviour("Move Towards", move_towards, ai_controller),
                                CustomBehaviour("Attack", attack, ai_controller)
                            ]
                        )
                    ]
                ),
                pt.composites.Sequence(
                    name="Defend Mode",
                    memory=False,
                    children=[
                        CustomBehaviour("Is Defend Mode", is_defend_mode, ai_controller),
                        pt.composites.Selector(
                            name="Defend Actions",
                            memory=False,
                            children=[
                                CustomBehaviour("Move Away", move_away, ai_controller),
                                CustomBehaviour("Jump", jump, ai_controller)
                            ]
                        )
                    ]
                )
            ]
        )

        self.tree = pt.trees.BehaviourTree(root)
        print(console.green + "AI Behavior Tree" + console.reset)
        print(pt.display.ascii_tree(self.tree.root))
