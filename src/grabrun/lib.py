import dataclasses
import datetime

import dateutil.relativedelta
import humanize

from . import timestamps


@dataclasses.dataclass
class Record:
    size: int
    filename: str
    timestamp: datetime.datetime

    def formatted_size(self):
        return humanize.naturalsize(self.size, binary=True)

    def get_age(self):
        current_time = datetime.datetime.now()
        age_timestamp = self.timestamp
        age = dateutil.relativedelta.relativedelta(current_time, age_timestamp)
        return self.format_relativedelta(age)

    @staticmethod
    def format_relativedelta(rd):
        formatted_age = ""
        if rd.years:
            formatted_age += f"{rd.years}y"
        if rd.months:
            formatted_age += f"{rd.months}mo"
        if rd.days:
            formatted_age += f"{rd.days}d"
        if rd.hours:
            formatted_age += f"{rd.hours}h"
        return formatted_age.rjust(15)

    def __str__(self):
        iso_timestamp = self.timestamp.isoformat() if self.timestamp else ""
        return f"{self.get_age().rjust(7)} {self.formatted_size().rjust(10)} {iso_timestamp} {self.filename}"  # noqa: E501


def main(args):
    with open(args.list_path, "r") as file:
        lines = file.readlines()

    records = []
    for line in lines:
        parts = line.strip().split()
        s3_timestamp = " ".join(parts[:2])
        size = int(parts[2])
        filename = " ".join(parts[3:])
        timestamp = timestamps.timestamp_extractor.extract_timestamp(
            filename
        ) or timestamps.timestamp_extractor.extract_timestamp(s3_timestamp)
        record = Record(size, filename, timestamp)
        records.append(record)

    if args.sort_by_size:
        sorted_by_size = sorted(records, key=lambda r: r.size, reverse=False)
        print("Sorted by File Size:")
        for record in sorted_by_size:
            print(record)

    elif args.sort_by_timestamp:
        sorted_by_timestamp = sorted(
            records, key=lambda r: (r.timestamp or datetime.datetime.min), reverse=False
        )
        print("Sorted by Timestamp:")
        for record in sorted_by_timestamp:
            print(record)
