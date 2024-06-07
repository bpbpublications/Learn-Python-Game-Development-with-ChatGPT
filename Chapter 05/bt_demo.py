import py_trees
import random

class AIController:
    def __init__(self):
        self.health = 100  # AI's starting health
        self.opponent_health = 100  # Opponent's starting health
        self.range = random.randint(1, 10)  # Random initial range
        self.attack_range = 3  # Attack range

    def update(self):
        # Simulate updating health, opponent's health, and range
        self.health -= random.randint(1, 10)
        self.opponent_health -= random.randint(1, 10)
        self.range = random.randint(1, 10)

# Define custom behavior nodes
class AttackMode(py_trees.behaviour.Behaviour):
    def __init__(self, name, controller):
        super(AttackMode, self).__init__(name)
        self.controller = controller

    def update(self):
        if self.controller.health > 0.5 * self.controller.health or self.controller.health > self.controller.opponent_health:
            self.feedback_message = "AI is in attack mode"
            return py_trees.common.Status.SUCCESS
        else:
            self.feedback_message = "AI is not in attack mode"
            return py_trees.common.Status.FAILURE

class DefendMode(py_trees.behaviour.Behaviour):
    def __init__(self, name, controller):
        super(DefendMode, self).__init__(name)
        self.controller = controller

    def update(self):
        if self.controller.health < 0.25 * self.controller.health:
            self.feedback_message = "AI is in defend mode"
            return py_trees.common.Status.SUCCESS
        else:
            self.feedback_message = "AI is not in defend mode"
            return py_trees.common.Status.FAILURE

class MoveTowardsOpponent(py_trees.behaviour.Behaviour):
    def __init__(self, name, controller):
        super(MoveTowardsOpponent, self).__init__(name)
        self.controller = controller

    def update(self):
        if self.controller.range > self.controller.attack_range:
            self.feedback_message = "Moving towards opponent"
            return py_trees.common.Status.SUCCESS
        else:
            self.feedback_message = "Not moving towards opponent"
            return py_trees.common.Status.FAILURE

class Attack(py_trees.behaviour.Behaviour):
    def __init__(self, name, controller):
        super(Attack, self).__init__(name)
        self.controller = controller

    def update(self):
        if self.controller.range < self.controller.attack_range:
            self.feedback_message = "Attacking opponent"
            return py_trees.common.Status.SUCCESS
        else:
            self.feedback_message = "Not attacking opponent"
            return py_trees.common.Status.FAILURE

class MoveAwayFromOpponent(py_trees.behaviour.Behaviour):
    def __init__(self, name, controller):
        super(MoveAwayFromOpponent, self).__init__(name)
        self.controller = controller

    def update(self):
        if self.controller.health < 0.25 * self.controller.health:
            self.feedback_message = "Moving away from opponent"
            return py_trees.common.Status.SUCCESS
        else:
            self.feedback_message = "Not moving away from opponent"
            return py_trees.common.Status.FAILURE

class Jump(py_trees.behaviour.Behaviour):
    def __init__(self, name, controller):
        super(Jump, self).__init__(name)
        self.controller = controller

    def update(self):
        if self.controller.range <= self.controller.attack_range:
            self.feedback_message = "Jumping to avoid opponent's attack"
            return py_trees.common.Status.SUCCESS
        else:
            self.feedback_message = "Not jumping"
            return py_trees.common.Status.FAILURE

# Create the behavior tree
def create_behavior_tree(controller):
    root = py_trees.composites.Selector("Root", True)
    
    attack_mode = AttackMode("Attack Mode", controller)
    defend_mode = DefendMode("Defend Mode", controller)
    
    attack_sequence = py_trees.composites.Sequence("Attack Sequence", True)
    move_towards_opponent = MoveTowardsOpponent("Move Towards Opponent", controller)
    attack = Attack("Attack", controller)
    
    defend_sequence = py_trees.composites.Sequence("Defend Sequence", True)
    move_away_from_opponent = MoveAwayFromOpponent("Move Away From Opponent", controller)
    jump = Jump("Jump", controller)
    
    root.children.extend([attack_mode, defend_mode])
    attack_mode.children.extend([attack_sequence])
    attack_sequence.children.extend([move_towards_opponent, attack])
    
    defend_mode.children.extend([defend_sequence])
    defend_sequence.children.extend([move_away_from_opponent, jump])
    
    return root

if __name__ == "__main__":
    ai_controller = AIController()
    behavior_tree = create_behavior_tree(ai_controller)
    tree = py_trees.trees.BehaviourTree(behavior_tree)
    
    for _ in range(10):  # Simulate 10 time steps
        ai_controller.update()  # Update AI state
        tree.tick()  # Tick the behavior tree
        print(f"Health: {ai_controller.health}, Range: {ai_controller.range}")
        print(tree.root.feedback_message)
