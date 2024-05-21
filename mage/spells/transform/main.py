import pyarrow as pa
import pandas as pd
import json
import s3fs
from pyarrow import Table, parquet as pq

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
from multiprocessing import Process

client = Minio('minio1:9000', access_key=base.ACCESS_KEY,
               secret_key=base.SECRET_KEY, secure=False)

minio = s3fs.S3FileSystem(key=base.ACCESS_KEY,
                          secret=base.SECRET_KEY,
                          use_ssl=False,
                          client_kwargs={
                              'endpoint_url': 'http://minio1:9000'
                          })
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
    # TODO: group by itertools and save the group in your
    #       respective processed level directory
    # ==================================================
    #df = pd.DataFrame(processed_spells)
    #table = Table.from_pandas(df)
    #pq.write_to_dataset(
    #    table,
    #    "s3://spells/processed",
    #    filesystem=minio,
    #    use_dictionary=True,
    #    compression="snappy",
    #    version="2.6"
    #)



if __name__ == '__main__':
    main()
