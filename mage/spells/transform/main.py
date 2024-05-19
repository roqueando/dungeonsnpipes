from minio import Minio
import json
import batch as transform_batch
import base
import description
import components
import range
import damage
import grouping
from multiprocessing import Process


def transform_data(batch):
    base.Transformer(batch=batch['spells']) \
        .apply(description.transform_description) \
        .apply(components.transform_components) \
        .apply(range.transform_range) \
        .apply(damage.transform_damage) \
        .apply(grouping.group_by_level)
    # .apply(saving.save_to_parquet)


def main():
    client = Minio('minio1:9000', access_key=base.ACCESS_KEY,
                   secret_key=base.SECRET_KEY, secure=False)
    try:
        response = client.get_object("spells", "spells.json")
        spells = json.loads(response.read())
        batches = transform_batch.turn_into_batches(spells)
        for batch in batches:
            proc = Process(target=transform_data, args=(batch,))
            proc.start()

    except:
        raise Exception("spells.json not found")


if __name__ == '__main__':
    main()
