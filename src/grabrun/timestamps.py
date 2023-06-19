import datetime
import re


class TimestampExtractor:
    def __init__(self):
        self.patterns = []

    def add_pattern(self, pattern):
        self.patterns.append(pattern)

    def extract_timestamp(self, filename):
        for pattern in self.patterns:
            matches = pattern.search(filename)
            if matches:
                year = int(matches.group("year"))
                month = int(matches.group("month"))
                day = int(matches.group("day"))
                hour = int(matches.group("hour"))
                minute = int(matches.group("minute"))
                second = (
                    int(matches.group("second"))
                    if "second" in matches.groupdict()
                    else 0
                )
                offset = (
                    int(matches.group("offset"))
                    if "offset" in matches.groupdict()
                    else 0
                )

                gmt_offset = datetime.timedelta(hours=offset)

                return (
                    datetime.datetime(year, month, day, hour, minute, second)
                    + gmt_offset
                )
        return None


# Create an instance of TimestampExtractor
timestamp_extractor = TimestampExtractor()

# Define the existing regex patterns and add them to the TimestampExtractor
existing_patterns = [
    re.compile(
        r"""
        (
            # 2021-04-22 at 11_01 GMT-7
            (?P<year>\d{4})-
            (?P<month>\d{2})-
            (?P<day>\d{2})
            \s
            at
            \s
            (?P<hour>\d{2})
            _
            (?P<minute>\d{2})
            \s
            GMT(?P<offset>-\d+)
        )
        """,
        re.VERBOSE,
    ),
    re.compile(
        r"""
        (
            # GMT20220909-181023
            (?P<year>\d{4})
            (?P<month>\d{2})
            (?P<day>\d{2})
            [_-]
            (?P<hour>\d{2})
            (?P<minute>\d{2})
            (?P<second>\d{2})
        )
        """,
        re.VERBOSE,
    ),
    re.compile(
        r"""
        (
            # 2022-05-29 17:52:23
            (?P<year>\d{4})
            -
            (?P<month>\d{2})
            -
            (?P<day>\d{2})
            [\s_-]
            (?P<hour>\d{2})
            :
            (?P<minute>\d{2})
            :
            (?P<second>\d{2})
        )
        """,
        re.VERBOSE,
    ),
]

for pattern in existing_patterns:
    timestamp_extractor.add_pattern(pattern)

# Add a new regex pattern for the additional timestamp format
new_pattern = re.compile(
    r"""
    (
        # New timestamp format
        # Modify this pattern according to the new format
        # (?P<new_group>\d{4}-\d{2}-\d{2})
        # ...
    )
    """,
    re.VERBOSE,
)

# timestamp_extractor.add_pattern(new_pattern)
