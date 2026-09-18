from collections import deque

processes = [
    {"pid": "P1", "arrival": 0, "burst": 7, "priority": 2},
    {"pid": "P2", "arrival": 2, "burst": 4, "priority": 1},
    {"pid": "P3", "arrival": 4, "burst": 1, "priority": 3},
    {"pid": "P4", "arrival": 5, "burst": 4, "priority": 2},
]


def priority_scheduling(process_list):
    current_time = 0
    completed = set()
    result = []

    while len(completed) < len(process_list):
        ready = [
            p for p in process_list
            if p["arrival"] <= current_time and p["pid"] not in completed
        ]

        if not ready:
            next_time = min(p["arrival"] for p in process_list if p["pid"] not in completed)
            result.append(("IDLE", current_time, next_time))
            current_time = next_time
            continue

        process = min(ready, key=lambda p: (p["priority"], p["arrival"], p["pid"]))
        start = current_time
        end = start + process["burst"]
        result.append((process["pid"], start, end))
        current_time = end
        completed.add(process["pid"])

    return result


def round_robin(process_list, quantum):
    if quantum <= 0:
        raise ValueError("Time quantum must be greater than zero.")

    remaining = [
        {"pid": p["pid"], "arrival": p["arrival"], "burst": p["burst"], "remaining": p["burst"]}
        for p in process_list
    ]
    queue = deque()
    current_time = 0
    completed = 0
    result = []

    while completed < len(remaining):
        for process in remaining:
            if process["arrival"] <= current_time and not process.get("done", False) and process["pid"] not in [p["pid"] for p in queue]:
                queue.append(process)

        if not queue:
            next_arrival = min(p["arrival"] for p in remaining if not p.get("done", False))
            result.append(("IDLE", current_time, next_arrival))
            current_time = next_arrival
            continue

        process = queue.popleft()
        start = current_time
        run_time = min(quantum, process["remaining"])
        current_time += run_time
        process["remaining"] -= run_time
        result.append((process["pid"], start, current_time))

        if process["remaining"] > 0:
            queue.append(process)
        else:
            process["done"] = True
            completed += 1

    return result


def show_result(title, intervals):
    print("\n" + title)
    print("Process Start End")

    sequence = []

    for pid, start, end in intervals:
        print(f"{pid:<9} {start:<7} {end}")

        if pid != "IDLE":
            sequence.append(pid)

    print("Sequence:", " -> ".join(sequence))


print("INPUT PROCESSES")
print("PID AT BT PT")

for process in processes:
    print(f'{process["pid"]:<5} {process["arrival"]:<4} {process["burst"]:<4} {process["priority"]}')

print("\nPriority Convention: Lower number = higher priority")
show_result("PRIORITY SCHEDULING", priority_scheduling(processes))

quantum = 2
print(f"\nTime Quantum: {quantum}")
show_result("ROUND ROBIN SCHEDULING", round_robin(processes, quantum))