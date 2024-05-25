from pyarrow import parquet as pq
import os
import sqlalchemy
from pyarrow import fs

MINIO_ACCESS_KEY = os.environ.get('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = os.environ.get('MINIO_SECRET_KEY')
MINIO_URL = os.environ.get('MINIO_URL')
MYSQL_URL = os.environ.get('MYSQL_URL')
# mysql+<drivername>://<username>:<password>@<server>:<port>/dbname

minio_fs_pa = fs.S3FileSystem(access_key=MINIO_ACCESS_KEY, secret_key=MINIO_SECRET_KEY,
                              scheme='http', endpoint_override=MINIO_URL)

def main():
    print("loading...")
    conn = sqlalchemy.create_engine("mysql+mysqlconnector://dnd:dnd_default_password@localhost:3306/dnd_default", echo=True)

    for i in range(0, 10):
        level_filename = f'level_{i}.parquet'
        df = pq.read_table(f'spells/processed/{level_filename}', filesystem=minio_fs_pa) \
            .to_pandas() \
            .rename(columns={"heal_at_slot_level": "value_at_slot_level"}) \
            .to_sql(name="spells", con=conn)

if __name__ == '__main__':
    main()
