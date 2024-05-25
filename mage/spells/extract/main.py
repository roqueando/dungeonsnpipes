from . import base
import json
from io import BytesIO
from minio import Minio
import minio
import os

MINIO_ACCESS_KEY = os.environ.get('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = os.environ.get('MINIO_SECRET_KEY')
MINIO_URL = os.environ.get('MINIO_URL')

client = Minio(MINIO_URL, access_key=MINIO_ACCESS_KEY,
               secret_key=MINIO_SECRET_KEY, secure=False)


def save_index_spell(folder: str, filename: str, data: dict):
    client.put_object(folder, filename, BytesIO(json.dumps(
        data).encode('utf-8')), length=-1, part_size=10*1024*1024)


def get_index_spell(spell: str):
    client.get_object("spells", f'indexes/{spell}.json')

def cache_all_spells(response):
    spells_json = json.loads(response.read())['results']
    for cached_spell in spells_json:
        index = cached_spell['index']
        print(f'getting index: {index}...')
        try:
            spell = get_index_spell(index)
            print('got cached spell: {index}')
        except:
            api_spell = base.get_api_spell_index(index)
            save_index_spell("spells", f'indexes/{index}.json', api_spell)

def main():
    try:
        response = client.get_object("spells", "spells.json")
        cache_all_spells(response)
    except minio.error.S3Error:
        print("extracting spells...")
        spells = base.get_spells_from_api()
        response = client.put_object("spells", "spells.json",
                                     BytesIO(json.dumps(spells).encode('utf-8')), length=-1, part_size=10*1024*1024)
        cache_all_spells(response)


if __name__ == '__main__':
    main()
