import py_trees
import random

# Mock AIController class to provide state information
class AIController:
    def __init__(self):
        self.opponent_range = random.uniform(0, 10)  # Mock opponent range
        self.attack_range = 3.0  # AI's attack range
        self.health = random.uniform(0, 100)  # Mock AI's health

    def update_state(self):
        # Mock updating state information
        self.opponent_range = random.uniform(0, 10)
        self.health = random.uniform(0, 100)

# Behavior to move toward the opponent when range > attack range and health > 25
class MoveTowardsOpponent(py_trees.behaviour.Behaviour):
    def __init__(self, controller):
        super(MoveTowardsOpponent, self).__init__("MoveTowardsOpponent")
        self.controller = controller

    def update(self):
        if self.controller.opponent_range > self.controller.attack_range and self.controller.health > 25:
            print("Moving toward the opponent")
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE

# Behavior to move away from the opponent when health is below 25%
class MoveAwayFromOpponent(py_trees.behaviour.Behaviour):
    def __init__(self, controller):
        super(MoveAwayFromOpponent, self).__init__("MoveAwayFromOpponent")
        self.controller = controller

    def update(self):
        if self.controller.health < 25:
            print("Moving away from the opponent")
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE

# Behavior to jump when opponent may attack
class Jump(py_trees.behaviour.Behaviour):
    def __init__(self, controller):
        super(Jump, self).__init__("Jump")
        self.controller = controller

    def update(self):
        if self.controller.opponent_range < self.controller.attack_range:
            print("Jumping to avoid opponent's attack")
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE

# Behavior to attack when range < attack range
class Attack(py_trees.behaviour.Behaviour):
    def __init__(self, controller):
        super(Attack, self).__init__("Attack")
        self.controller = controller

    def update(self):
        if self.controller.opponent_range < self.controller.attack_range:
            print("Attacking the opponent")
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE

def create_behavior_tree(controller):
    root = py_trees.composites.Sequence("Root", True)

    move_toward_opponent = MoveTowardsOpponent(controller)
    move_away_from_opponent = MoveAwayFromOpponent(controller)
    jump = Jump(controller)
    attack = Attack(controller)

    root.add_children([move_toward_opponent, move_away_from_opponent, jump, attack])

    return py_trees.trees.BehaviourTree(root)

if __name__ == "__main__":
    controller = AIController()
    behavior_tree = create_behavior_tree(controller)

    while True:
        controller.update_state()
        behavior_tree.tick()
