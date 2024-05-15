import dungeonsnpipes.extract.api_extractor as api_extractor
import dungeonsnpipes.transform.transform as transformer

def main():
    print("extracting spells...")
    spells = api_extractor.get_spells_from_api()
    batches = transformer.turn_into_batches(spells)

    for batch in batches:
        print(f'spell count: {len(batch.spells)}')

main()
