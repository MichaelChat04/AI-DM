import random
import json

class AIDungeonMaster:
    def __init__(self):
        self.memory = {
            "players": {},
            "story_progress": [],
            "npc_interactions": {},
        }

    def roll_dice(self, dice: str):
        """Simulates dice rolls (e.g., '1d20' or '3d6')."""
        num, sides = map(int, dice.lower().split('d'))
        rolls = [random.randint(1, sides) for _ in range(num)]
        return sum(rolls), rolls

    def generate_npc(self, name):
        """Creates a random NPC with personality traits."""
        personalities = ["Friendly", "Hostile", "Cunning", "Mysterious", "Loyal", "Untrustworthy"]
        role = ["Merchant", "Knight", "Wizard", "Assassin", "Bard", "Bandit"]
        self.memory["npc_interactions"][name] = {
            "personality": random.choice(personalities),
            "role": random.choice(role),
            "history": []
        }
        return self.memory["npc_interactions"][name]

    def generate_quest(self):
        """Generates a random quest for players."""
        quest_types = ["Rescue", "Assassinate", "Retrieve", "Defend", "Explore"]
        locations = ["Ancient Ruins", "Haunted Forest", "Dwarven Mines", "Royal Castle", "Abandoned Village"]
        rewards = ["Gold", "Magic Item", "Favor of a Noble", "Mystical Knowledge"]
        
        quest = {
            "type": random.choice(quest_types),
            "location": random.choice(locations),
            "reward": random.choice(rewards),
        }
        self.memory["story_progress"].append(quest)
        return quest

    def player_action(self, player, action):
        """Handles a player's action and generates a dynamic response."""
        if player not in self.memory["players"]:
            self.memory["players"][player] = {"actions": []}

        self.memory["players"][player]["actions"].append(action)

        # Example responses based on action types
        if "attack" in action:
            roll, details = self.roll_dice("1d20")
            return f"{player} attempts an attack and rolls {roll} ({details})."

        elif "explore" in action:
            location = random.choice(["a hidden cave", "an ancient temple", "a forgotten battlefield"])
            return f"{player} explores {location} and discovers something unusual."

        elif "talk" in action:
            npc_name = action.split(" ")[-1].capitalize()
            if npc_name not in self.memory["npc_interactions"]:
                npc = self.generate_npc(npc_name)
            else:
                npc = self.memory["npc_interactions"][npc_name]

            return f"{player} talks to {npc_name}. They seem {npc['personality']} and introduce themselves as a {npc['role']}."

        return f"{player} performs {action}, and the world reacts accordingly."

# Create the AI DM instance and run some sample interactions
ai_dm = AIDungeonMaster()

# Example interactions
quest = ai_dm.generate_quest()
npc_interaction = ai_dm.player_action("Michael", "talk to Marcus")
attack_result = ai_dm.player_action("Michael", "attack the goblin")

# Display the generated responses
quest, npc_interaction, attack_result

print("AI Dungeon Master is running!")
