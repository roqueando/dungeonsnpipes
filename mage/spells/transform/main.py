import itertools
from minio import Minio
from minio.datatypes import Object
import json
from . import batch as transform_batch
from . import base
from . import description
from . import components
from . import range as transform_range
from . import damage
from . import grouping
from multiprocessing import Process

client = Minio('minio1:9000', access_key=base.ACCESS_KEY,
               secret_key=base.SECRET_KEY, secure=False)

def get_spell_by_index(spell: str):
    client.get_object("spells", f'indexes/{spell}.json')

def transform_data(obj: Object) -> dict:
    obj_content = client.get_object("spells", obj.object_name)
    json_obj = json.loads(obj_content.read())

    processed = base.Transformer(spell=json_obj) \
        .apply(description.transform_description) \
        .apply(components.transform_components) \
        .apply(transform_range.transform_range) \
        .apply(damage.transform_damage)
    return processed.spell


def main():

    objects = client.list_objects("spells", prefix="indexes", recursive=True)

    processed_spells = list(map(transform_data, objects))
    print(processed_spells[0])

    #try:
    #    response = client.get_object("spells", "spells.json")
    #    spells = json.loads(response.read())
    #    batches = transform_batch.turn_into_batches(spells)
    #    new_batches = []
    #    groups = []
    #    for batch in batches:
    #        new_batch = transform_data(batch=batch)
    #        new_batches += new_batch
    #        # proc = Process(target=transform_data, args=(batch,))
    #        # proc.start()
    #        # data = proc.join()
    #        # print(data)
    #    for k, g in itertools.groupby(new_batches, lambda x: x['level']):
    #        groups.append({str(k): list(g)})
    #    print(groups)
    #except:
    #    raise Exception("spells.json not found")


if __name__ == '__main__':
    main()
