import csv


def iter_csv(data):
    writer = csv.writer
    yield ",".join(["city", "unit", "temperature", "description", "timestamp", "served_from_cache"]) + "\n"
    for row in data:
        yield ",".join([
            str(row["city"]),
            str(row["unit"]),
            str(row["temperature"]),
            str(row["description"]),
            row["timestamp"].isoformat(),
            str(row["served_from_cache"])
        ]) + "\n"