import dungeonsnpipes.extract.api_extractor as api_extractor
import dungeonsnpipes.transform.transform as transformer
from multiprocessing import Process

def main():
    print("extracting spells...")
    spells = api_extractor.get_spells_from_api()
    batches = transformer.turn_into_batches(spells)

    print("transforming...")
    for batch in batches:
        proc = Process(target=execute_transformer, args=(batch,))
        proc.start()

def execute_transformer(batch: transformer.SpellBatch):
    return transformer.Transformer(batch=batch.spells) \
            .apply(transformer.transform_description) \
            .apply(transformer.transform_components) \
            .apply(transformer.transform_range) \
            .apply(transformer.transform_damage)

if __name__ == '__main__':
    main()
