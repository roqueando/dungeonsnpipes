from pyarrow import parquet as pq
from minio import Minio
from minio.datatypes import Object
from io import BytesIO
from . import batch as transform_batch
from . import base
from . import description
from . import components
from . import range as transform_range
from . import damage
from . import grouping
from pyarrow import fs

import os
import minio
import pandas as pd
import pyarrow as pa
import json

MINIO_ACCESS_KEY = os.environ.get('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = os.environ.get('MINIO_SECRET_KEY')
MINIO_URL = os.environ.get('MINIO_URL')

client = Minio(MINIO_URL, access_key=MINIO_ACCESS_KEY,
               secret_key=MINIO_SECRET_KEY, secure=False)

minio_fs_pa = fs.S3FileSystem(access_key=MINIO_ACCESS_KEY, secret_key=MINIO_SECRET_KEY,
                              scheme='http', endpoint_override=MINIO_URL)


def get_spell_by_index(spell: str):
    client.get_object("spells", f'indexes/{spell}.json')

def save_level_group(filename: str, data: dict):
    new_dict = {}
    for key, value in data.items():
        new_dict[key] = [value]

    table = pa.table(new_dict)
    pq.write_table(table, f'spells/processed/{filename}', filesystem=minio_fs_pa)


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
    print('transforming...')

    objects = client.list_objects("spells", prefix="indexes", recursive=True)
    processed_spells = list(map(transform_data, objects))
    grouped = grouping.group_by_level(processed_spells)

    for group in grouped:
        level = list(group.keys())[0]
        level_filename = f'level_{level}.parquet'

        try:
            df = pq.read_table(f'spells/processed/{level_filename}', filesystem=minio_fs_pa) \
                .to_pandas()
            df2 = pd.DataFrame(group[level])
            df = pd.concat([df, df2])
            from_pandas = pa.Table.from_pandas(df)

            pq.write_table(from_pandas,
                           f'spells/processed/{level_filename}',
                           filesystem=minio_fs_pa)

            # INFO: probably writing to dataset is more efficient or not? I'll try later
            #pq.write_to_dataset(pa.Table.from_pandas(df),
            #                    f"spells/processed/{level_filename}",
            #                    filesystem=minio_fs_pa)
        except FileNotFoundError:
            save_level_group(level_filename, group)

    print('finishing...')


if __name__ == '__main__':
    main()
