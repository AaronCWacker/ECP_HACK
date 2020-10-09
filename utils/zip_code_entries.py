import definitions
import pandas as pdb
from typing import NamedTuple, Dict

_ROOT_DIR = definitions.get_project_root()


class ZipCodeEntry(NamedTuple):
    zip: str
    city: str
    state: str
    lat: str
    long: str
    time_zone: str
    dst_flags: bool


def _load_zip_codes() -> Dict[str, ZipCodeEntry]:
    df = pdb.read_csv(f'{_ROOT_DIR}/utils/us-zip-code-latitude-and-longitude.txt', dtype=str,
                      sep=';')
    zip_code_list = {}
    # Zip;City;State;Latitude;Longitude;Timezone;Daylight savings time flag;geopoint
    for _, row in df.iterrows():
        zip_code = row.get('Zip')
        if zip_code:
            zip_code_entry = ZipCodeEntry(
                zip=zip_code,
                city=row.get('City'),
                state=row.get('State'),
                lat=row.get('Latitude'),
                long=row.get('Longitude'),
                time_zone=row.get('Timezone'),
                dst_flags=row.get('Daylight savings time flag')
            )
            zip_code_list[zip_code] = zip_code_entry

    return zip_code_list


ZIP_CODE_LIST = _load_zip_codes()


if __name__ == '__main__':
    print(ZIP_CODE_LIST)
    print(ZIP_CODE_LIST.get('62833'))

