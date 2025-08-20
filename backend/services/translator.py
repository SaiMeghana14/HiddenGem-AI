import json, os
from typing import Optional
PHRASEBOOK = json.load(open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "data", "phrasebook.json"), encoding="utf-8"))

def translate(text: str, src: str, dest: str) -> Optional[str]:
    key = f"{src}->{dest}"
    if key in PHRASEBOOK and text in PHRASEBOOK[key]:
        return PHRASEBOOK[key][text]
    return None  # fallback to external API in future
