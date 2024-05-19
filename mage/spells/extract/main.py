from . import base
import json
from io import BytesIO
from minio import Minio


def save_object(folder: str, filename: str):
    client.put_object(folder, filename)


def main():
    client = Minio('minio1:9000', access_key=base.ACCESS_KEY,
                   secret_key=base.SECRET_KEY, secure=False)
    try:
        response = client.get_object("spells", "spells.json")
        if response:
            spells_json = json.loads(response.read())
            for k, v in spells_json.iter():
                if k == 'index':
                    spell = base.get_api_spell_index(v)
                    # get spell from index and save as {index-name}.json
        return 'spells.json'
    except Exception as err:
        spells = base.get_spells_from_api()
        client.put_object("spells", "spells.json",
                          BytesIO(json.dumps(spells).encode('utf-8')), length=-1, part_size=10*1024*1024)


if __name__ == '__main__':
    main()
