from wiktionaryparser import WiktionaryParser
from app.models.dictionary import NounInfoResponse

parser = WiktionaryParser()
parser.set_default_language('german')

def get_noun_info(noun: str) -> NounInfoResponse:
    try:
        entries = parser.fetch(noun)
        if not entries or not entries[0].get('definitions'):
            return NounInfoResponse(noun=noun, error="No data found for this noun.")
        definitions = entries[0]['definitions'][0]
        gender = None
        plural = None
        # Gender: Try to extract from definition text, typical patterns: "f", "m", "n", "die", "der", "das"
        if 'text' in definitions and definitions['text']:
            for line in definitions['text']:
                # Try to match "die Katze", "der Hund" etc.
                if line.lower().startswith(("die ", "der ", "das ")):
                    gender = line.split()[0].lower()
                    break
                if "Genus:" in line:
                    # e.g., "Genus: f"
                    g = line.split("Genus:", 1)[-1].strip().lower()
                    if g in ("f", "feminine"):
                        gender = "die"
                    elif g in ("m", "masculine"):
                        gender = "der"
                    elif g in ("n", "neuter"):
                        gender = "das"
        # Plural is often in relatedWords
        for related in definitions.get('relatedWords', []):
            if related['relationshipType'].lower() == 'plural' and related['words']:
                plural = related['words'][0]
        return NounInfoResponse(noun=noun, gender=gender, plural=plural)
    except Exception as e:
        return NounInfoResponse(noun=noun, error=str(e))
