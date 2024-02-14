from functools import cache
from pathlib import Path

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand

from points_of_interests.management.file_readers import CsvReader, JsonReader, XmlReader
from points_of_interests.models import Poi, Category

file_handlers = {
    ".csv": CsvReader,
    ".json": JsonReader,
    # ".xml": XmlReader,  # TODO implement XML reader
}


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("filepath", type=str, help="The path to the file to upload")

    @cache
    def get_or_create_category(self, name: str) -> Category:
        return Category.objects.get_or_create(name=name)

    def handle(self, *args, **kwargs):
        file_path = Path(kwargs["filepath"])
        if not file_path.exists():
            raise FileNotFoundError(f"File not found at {file_path}")

        # parse the name
        ext = file_path.suffix

        # match file extension to file handler
        try:
            file_reader_klass = file_handlers[ext]
        except KeyError:
            raise ValueError(f"Unsupported file type {ext}. Should be one of {list(file_handlers.keys())}")

        # use file handler to read data from file
        with file_path.open("r") as file:
            reader = file_reader_klass(file)

            # upload data to database, line by line
            # TODO: use bulk create, batch ~1000 lines at a time
            for line in reader.readlines():
                cat, _ = self.get_or_create_category(line["category"])

                # - create poi
                try:
                    Poi.objects.create(
                        external_id=line["external_id"],
                        name=line["name"],
                        latitude=line["latitude"],
                        longitude=line["longitude"],
                        category=cat,
                        ratings=line["ratings"],
                        description=line["description"],
                    )
                except ValidationError as e:
                    breakpoint()
                    self.stderr.write(f"Error creating POI {line}: {e}")
                    continue
