import random

_GREETINGS = [
    "Hey there! Ctrl + C, Ctrl + V some coding fun!",
    "Greetings, fellow coder! Ready to rock some bytes?",
    "Beep boop! Welcome to Mochi, where coding dreams come true! 💻✨",
    "Hasta la vista, buggy code! Welcome to Mochi! 🎉",
    ("G'day, human! Let's code like it's binary o'clock! 01010111 01100101 "
     "01101100 01100011 01101111 01101101 01100101 00100001"),
    ("Ahoy, matey! Prepare to set sail in the sea of code with Mochi as "
     "your trusty parrot! 🏴‍☠️💻"),
    ("Greetings, Earthling! Mochi is here to help you conquer the coding "
     "universe, one line at a time! 🚀💫"),
    ("Yo, coderino! Welcome to Mochi, the secret lair of coding "
     "awesomeness! 🕶️💻"),
    ("Buckle up, coding adventurer! Mochi is about to take you on a wild "
     "ride through the enchanted land of code! 🎢💻"),
    ("Aloha, coding friend! Get ready for some tropical vibes and "
     "bug-crushing adventures with Mochi! 🌺💻")
]

_HELP_PROMPTS = [
    "How can I help you?",
    "What can I do for you?",
    "Need any assistance?",
    "How may I be of service?",
    "What do you need help with?",
    "What task can I help you with?"
]

_WAIT_MESSAGES = [
    "On it!",
    "Working on it...",
    "Give me a moment...",
    "Just a second...",
    "Hang tight!",
    "Processing your request...",
    "Hold on...",
    "Almost there...",
    "Please wait...",
    "Getting things ready...",
    "Stand by...",
    "Let me think...",
    "Working my magic...",
    "Stay with me..."
]


def get_greeting() -> str:
    """Get a greeting."""
    greeting = random.choice(_GREETINGS)
    helpful = random.choice(_HELP_PROMPTS)
    return f"🤖{greeting}\n🤖{helpful}"


def get_waiting_message() -> str:
    """Get a message to display while waiting for responses."""
    return random.choice(_WAIT_MESSAGES)
