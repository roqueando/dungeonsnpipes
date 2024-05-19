import itertools
from minio import Minio
import json
from . import batch as transform_batch
from . import base
from . import description
from . import components
from . import range
from . import damage
from . import grouping
from multiprocessing import Process


def transform_data(batch):
    base.Transformer(batch=batch['spells']) \
        .apply(description.transform_description) \
        .apply(components.transform_components) \
        .apply(range.transform_range) \
        .apply(damage.transform_damage)
    # .apply(grouping.group_by_level)
    # .apply(saving.save_to_parquet)


def main():
    client = Minio('minio1:9000', access_key=base.ACCESS_KEY,
                   secret_key=base.SECRET_KEY, secure=False)
    try:
        response = client.get_object("spells", "spells.json")
        spells = json.loads(response.read())
        batches = transform_batch.turn_into_batches(spells)
        new_batches = []
        groups = []
        for batch in batches:
            new_batch = transform_data(batch=batch)
            new_batches += new_batch
            # proc = Process(target=transform_data, args=(batch,))
            # proc.start()
            # data = proc.join()
            # print(data)
        for k, g in itertools.groupby(new_batches, lambda x: x['level']):
            groups.append({str(k): list(g)})
        print(groups)
    except:
        raise Exception("spells.json not found")


if __name__ == '__main__':
    main()
