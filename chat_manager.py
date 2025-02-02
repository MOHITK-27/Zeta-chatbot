import re
import random
from pr import PERSONALITY_TRAITS, PREDEFINED_RESPONSES

def get_predefined_response(user_input):
    user_input = user_input.lower()
    for category, data in PREDEFINED_RESPONSES.items():
        for pattern in data["patterns"]:
            if re.search(pattern, user_input, re.IGNORECASE):
                return random.choice(data["responses"])
    return None

def process_think_blocks(response):
    processed_response = re.sub(
        r'<think>(.*?)</think>',
        r'<div class="thinking-block">\1</div>',
        response,
        flags=re.DOTALL
    )
    return processed_response

def format_response(predefined_response):
    prefix = random.choice(PERSONALITY_TRAITS["catchphrases"])
    return f"{prefix} {predefined_response}"