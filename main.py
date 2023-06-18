import dataclasses
import datetime

import dateutil.relativedelta
import humanize


@dataclasses.dataclass
class Record:
    s3_timestamp: datetime.datetime
    size: int
    filename: str
    timestamp: datetime.datetime

    def formatted_size(self):
        return humanize.naturalsize(self.size, binary=True)

    def get_age(self):
        current_time = datetime.datetime.now()
        age_timestamp = self.timestamp or self.s3_timestamp
        age = dateutil.relativedelta.relativedelta(current_time, age_timestamp)
        return self.format_relativedelta(age)

    @staticmethod
    def extract_timestamp(filename):
        parts = filename.split("-")
        if len(parts) > 1:
            timestamp_str = parts[1].split("_")[0]
            try:
                return datetime.datetime.strptime(timestamp_str, "%Y%m%d%H%M%S")
            except ValueError:
                pass
        # Check if the filename matches the alternative format
        if "Video-" in filename:
            parts = filename.split("-")
            timestamp_str = parts[1]
            try:
                return datetime.datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
            except ValueError:
                pass
        return None

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
        iso_timestamp = (
            self.timestamp.isoformat()
            if self.timestamp
            else self.s3_timestamp.isoformat()
        )
        return f"{self.get_age().rjust(7)} {self.formatted_size().rjust(10)} {iso_timestamp} {self.filename}"  # noqa: E501


with open("list.txt", "r") as file:
    lines = file.readlines()

records = []
for line in lines:
    parts = line.strip().split()
    s3_timestamp = datetime.datetime.strptime(
        parts[0] + " " + parts[1], "%Y-%m-%d %H:%M:%S"
    )
    size = int(parts[2])
    filename = parts[3]
    timestamp = Record.extract_timestamp(filename)
    record = Record(s3_timestamp, size, filename, timestamp)
    records.append(record)


# Sort records by file size
sorted_by_size = sorted(records, key=lambda r: r.size)
print("Sorted by File Size:")
for record in sorted_by_size:
    print(record)

# Sort records by timestamp
sorted_by_timestamp = sorted(
    records, key=lambda r: (r.timestamp or r.s3_timestamp), reverse=False
)
print("Sorted by Timestamp:")
for record in sorted_by_timestamp:
    print(record)
