from . import base
import json
from io import BytesIO
from minio import Minio

client = Minio('minio1:9000', access_key=base.ACCESS_KEY,
               secret_key=base.SECRET_KEY, secure=False)

def save_index_spell(folder:str, filename: str, data: dict):
    client.put_object(folder, filename, BytesIO(json.dumps(data).encode('utf-8')), length=-1, part_size=10*1024*1024)

def get_index_spell(spell: str):
    client.get_object("spells", f'indexes/{spell}.json')


def main():
    response = client.get_object("spells", "spells.json")
    if response:
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
    else:
        spells = base.get_spells_from_api()
        client.put_object("spells", "spells.json",
                          BytesIO(json.dumps(spells).encode('utf-8')), length=-1, part_size=10*1024*1024)


if __name__ == '__main__':
    main()
