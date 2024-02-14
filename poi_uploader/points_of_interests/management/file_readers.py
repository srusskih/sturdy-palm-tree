import csv
import json

from defusedxml.minidom import parse

from abc import ABCMeta, abstractmethod
from collections.abc import Iterator


class BaseReader(metaclass=ABCMeta):

    def __init__(self, fd):
        self.fd = fd

    @abstractmethod
    def readlines(self) -> Iterator[dict]:
        """Read lines from the file and return a dictionary of the data"""


def rating_parser(ratings: str) -> list[float]:
    return [float(r) for r in ratings.strip('{}').split(",")]


class CsvReader(BaseReader):

    def _remap(self, row: dict) -> dict:
        return {
            "external_id": row["poi_id"],
            "name": row["poi_name"],
            "latitude": row["poi_latitude"],
            "longitude": row["poi_longitude"],
            "category": row["poi_category"],
            "ratings": rating_parser(row["poi_ratings"]),
            "description": row["description"],
        }

    def readlines(self) -> Iterator[dict]:
        reader = csv.DictReader(self.fd)
        for row in reader:
            yield self._remap(row)


class JsonReader(BaseReader):

    def _remap(self, row: dict) -> dict:
        return {
            "external_id": row["id"],
            "name": row["name"],
            "latitude": row["coordinates"]["latitude"],
            "longitude": row["coordinates"]["longitude"],
            "category": row["category"],
            "ratings": row["ratings"],
            "description": row["description"],
        }

    def readlines(self) -> Iterator[dict]:
        data = json.load(self.fd)
        for row in data:
            yield self._remap(row)


class XmlReader(BaseReader):

    def readlines(self) -> Iterator[dict]:
        raise NotImplementedError("XMLReader not implemented yet")

        et = parse(self.fd)
        records = et.getElementsByTagName("RECORDS")
        for record in records:
            _r = record.getElementsByTagName("DATA_RECORD")[0]
            d = {
                "external_id": _r.getElementsByTagName("pid"),
                "name": _r.getElementsByTagName("pname"),
                "latitude": _r.getElementsByTagName("platitude"),
                "longitude": _r.getElementsByTagName("plongitude"),
                "category": _r.getElementsByTagName("pcategory"),
                "ratings": _r.getElementsByTagName("pratings"),
            }
            yield d
