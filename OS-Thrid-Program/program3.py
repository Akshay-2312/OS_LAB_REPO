processes = [
    {"pid": "P1", "arrival": 0, "brust": 7, "priority": 2},
    {"pid": "P2", "arrival": 2, "brust": 4, "priority": 1},
    {"pid": "P3", "arrival": 4, "brust": 1, "priority": 3},
    {"pid": "P4", "arrival": 5, "brust": 4, "priority": 2},
]


def print_table(title, rows, headers):
    widths = [len(str(header)) for header in headers]
    for row in rows:
        for i, value in enumerate(row):
            widths[i] = max(widths[i], len(str(value)))

    def format_row(values):
        return " | ".join(str(value).ljust(widths[i]) for i, value in enumerate(values))

    border = "-+-".join("-" * width for width in widths)
    print(f"\n{title}")
    print(format_row(headers))
    print(border)
    for row in rows:
        print(format_row(row))


def priority_scheduling(processes):
    current_time = 0
    completed = set()
    result = []

    while len(completed) < len(processes):
        ready = [p for p in processes if p["arrival"] <= current_time and p["pid"] not in completed]
        if not ready:
            next_time = min(p["arrival"] for p in processes if p["pid"] not in completed)
            result.append(("IDLE", current_time, next_time))
            current_time = next_time
            continue

        p = min(ready, key=lambda p: (p["priority"], p["arrival"], p["pid"]))
        start = current_time
        end = start + p["brust"]
        result.append((p["pid"], start, end))
        current_time = end
        completed.add(p["pid"])

    return result


if __name__ == "__main__":
    process_rows = [(p["pid"], p["arrival"], p["brust"]) for p in processes]
    print_table("Process Table: Process AT BT", process_rows, ["Process", "AT", "BT"])

    schedule = priority_scheduling(processes)
    print_table("Priority Scheduling Result", schedule, ["Process", "Start", "End"])
