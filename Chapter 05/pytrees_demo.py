import py_trees as pt
import py_trees.console as console

class AIController:
    def __init__(self, health, opponent_health, range_to_opponent, attack_range):
        self.health = health
        self.opponent_health = opponent_health
        self.range_to_opponent = range_to_opponent
        self.attack_range = attack_range

def is_attack_mode(ai_controller):
    if ai_controller.health > 50 or ai_controller.health > ai_controller.opponent_health:
        print("AI is in attack mode.")
        return pt.common.Status.SUCCESS
    else:
        return pt.common.Status.FAILURE

def is_defend_mode(ai_controller):
    if ai_controller.health <= 50 and ai_controller.health <= ai_controller.opponent_health:
        print("AI is in defend mode.")
        return pt.common.Status.SUCCESS
    else:
        return pt.common.Status.FAILURE

def move_towards(ai_controller):
    if ai_controller.range_to_opponent > ai_controller.attack_range:
        print("AI is moving towards the opponent.")
        return pt.common.Status.SUCCESS
    else:
        return pt.common.Status.FAILURE

def attack(ai_controller):
    if ai_controller.range_to_opponent <= ai_controller.attack_range:
        print("AI is attacking the opponent.")
        return pt.common.Status.SUCCESS
    else:
        return pt.common.Status.FAILURE

def move_away(ai_controller):
    if ai_controller.health < 25:
        print("AI is moving away from the opponent.")
        return pt.common.Status.SUCCESS
    else:
        return pt.common.Status.FAILURE

def jump(ai_controller):
    if ai_controller.range_to_opponent <= ai_controller.attack_range:
        print("AI is jumping.")
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

if __name__ == '__main__':
    ai_controller = AIController(health=60, opponent_health=50, range_to_opponent=10, attack_range=5)

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

    tree = pt.trees.BehaviourTree(root)
    print(console.green + "AI Behavior Tree" + console.reset)
    print(pt.display.ascii_tree(tree.root))

    for i in range(10):
        tree.tick()
