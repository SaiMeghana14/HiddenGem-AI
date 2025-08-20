import json, os
from typing import Tuple
from deep_translator import GoogleTranslator

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "data"))
PHRASEBOOK = json.load(open(os.path.join(DATA_DIR, "phrasebook.json"), encoding="utf-8"))

def _phrasebook(text: str, src: str, dest: str):
    key = f"{src}->{dest}"
    if key in PHRASEBOOK and text in PHRASEBOOK[key]:
        return PHRASEBOOK[key][text]
    return None

def translate(text: str, src: str, dest: str) -> Tuple[str, str]:
    # 1) Phrasebook direct match
    if src != "auto":
        pb = _phrasebook(text, src, dest)
        if pb:
            return pb, "phrasebook"
    else:
        # check all pairs that end with dest
        for key, mapping in PHRASEBOOK.items():
            if key.endswith(f"->{dest}") and text in mapping:
                return mapping[text], "phrasebook"

    # 2) Fallback to GoogleTranslator (no key needed)
    try:
        gt = GoogleTranslator(source=src, target=dest).translate(text)
        return gt, "google"
    except Exception:
        return text, "fallback"
