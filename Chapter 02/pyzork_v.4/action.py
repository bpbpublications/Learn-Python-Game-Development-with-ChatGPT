# action.py
class Action:
    def __init__(self, name, description, verbs, context=None):
        self.name = name
        self.description = description
        self.verbs = verbs
        self.context = context

    def can_execute(self, player, obj):
        # Check if the action can be executed based on the context.
        if self.context is None:
            return True
        if self.context == "inventory":
            return obj in player.inventory
        # Add more context checks as needed.

    def execute(self, player, obj):
        # Execute the action.
        pass