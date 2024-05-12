from dungeonsnpipes.extract.api_extractor import SpellResponse

class SpellBatch:
    MAX_SIZE = 10
    def __init__(self):
        self.spells = []


def turn_into_batches(response: SpellResponse) -> list[SpellBatch]:
    """Get the SpellResponse object and create a list of batches"""

    return []
    # TODO: aaaaaaaaaaa
