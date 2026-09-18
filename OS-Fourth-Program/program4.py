import os
import subprocess
import sys


def print_table(title, rows, widths=(30, 25, 35)):
    """Print rows as a clean ASCII table."""
    print(f"\n{title}")
    print("+" + "-" * (widths[0] + 2) + "+" + "-" * (widths[1] + 2) + "+" + "-" * (widths[2] + 2) + "+")
    print(f"| {'Field':<{widths[0]}} | {'Value':<{widths[1]}} | {'Details':<{widths[2]}} |")
    print("+" + "-" * (widths[0] + 2) + "+" + "-" * (widths[1] + 2) + "+" + "-" * (widths[2] + 2) + "+")
    for row in rows:
        field, value, detail = row
        print(f"| {field:<{widths[0]}} | {str(value):<{widths[1]}} | {detail:<{widths[2]}} |")
    print("+" + "-" * (widths[0] + 2) + "+" + "-" * (widths[1] + 2) + "+" + "-" * (widths[2] + 2) + "+")


def safe_display_proc_status():
    """Read a read-only /proc entry and display selected evidence."""
    try:
        with open("/proc/self/status", "r", encoding="utf-8") as proc_file:
            proc_lines = proc_file.readlines()
        status_info = {}
        for line in proc_lines:
            if line.startswith(("Pid:", "PPid:")):
                key, value = line.split(":", 1)
                status_info[key.strip()] = value.strip()
        return status_info
    except OSError as exc:
        return {"Error": str(exc)}


def create_and_verify_test_file():
    file_path = "/tmp/os_lab_test_file.txt"
    content = "Operating Systems Lab - process and file demo\n"

    try:
        with open(file_path, "w", encoding="utf-8") as file_obj:
            file_obj.write(content)

        with open(file_path, "r", encoding="utf-8") as file_obj:
            read_back = file_obj.read()

        return file_path, read_back.strip(), "File created and verified successfully"
    except OSError as exc:
        return file_path, "", f"File error: {exc}"


def demo_invalid_path():
    invalid_path = "/nonexistent_dir/invalid_test_file.txt"
    try:
        with open(invalid_path, "r", encoding="utf-8") as file_obj:
            file_obj.read()
    except OSError as exc:
        return invalid_path, f"Error: {exc}"
    return invalid_path, "Unexpected success"


def main():
    print("=" * 110)
    print("System Calls and Process Creation")
    print("=" * 110)

    print_table(
        "Overview",
        [
            ("Requirement", "Process creation", "Use os.fork() to create a child process"),
            ("Requirement", "Process IDs", "Display Child PID and Parent PID"),
            ("Requirement", "Wait", "Use os.waitpid() to wait for child completion"),
            ("Requirement", "Command", "Execute a harmless Linux command from the child"),
            ("Requirement", "File", "Create, write, read, and close a controlled test file"),
            ("Requirement", "Device Interface", "Read /dev/null and /proc/self/status evidence"),
            ("Requirement", "Error Handling", "Catch invalid path / file operation failure"),
        ],
        widths=(30, 30, 40),
    )

    parent_pid = os.getpid()
    print_table(
        "Parent Process Before Fork",
        [("Current PID", parent_pid, "Parent process started"), ("Method", "os.fork()", "Approved UNIX process creation mechanism")],
        widths=(30, 25, 40),
    )

    child_pid = os.fork()

    if child_pid == 0:
        child_pid_actual = os.getpid()
        parent_pid_actual = os.getppid()
        print_table(
            "Child Process Details",
            [
                ("Child PID", child_pid_actual, "New child process created"),
                ("Parent PID", parent_pid_actual, "Immediate parent id"),
                ("Process State", "Running", "Child executes task logic"),
            ],
            widths=(30, 25, 40),
        )

        file_path, file_content, file_status = create_and_verify_test_file()
        print_table(
            "File Handling Evidence",
            [
                ("File Path", file_path, "Controlled test file"),
                ("Written Data", file_content, "Read back successfully"),
                ("Status", file_status, "File was opened, written, read and closed"),
            ],
            widths=(30, 35, 35),
        )

        try:
            ls_result = subprocess.run(
                ["ls", "-l", "/tmp"],
                capture_output=True,
                text=True,
                check=True,
            )
            print_table(
                "Harmless Linux Command Output",
                [("Command", "ls -l /tmp", "Executed from child process"), ("Output", "Success", ls_result.stdout.splitlines()[0])],
                widths=(30, 25, 40),
            )
        except subprocess.CalledProcessError as exc:
            print_table(
                "Harmless Linux Command Output",
                [("Command", "ls -l /tmp", "Failed during execution"), ("Error", exc.returncode, exc.stderr.strip())],
                widths=(30, 25, 40),
            )

        try:
            with open("/dev/null", "w", encoding="utf-8") as dev_null:
                dev_null.write("This write is directed to /dev/null\n")
            dev_null_status = "Write successful"
        except OSError as exc:
            dev_null_status = f"Error: {exc}"

        proc_status = safe_display_proc_status()
        print_table(
            "Device Interface and /proc Check",
            [
                ("Device", "/dev/null", dev_null_status),
                ("Proc Status", proc_status.get("Pid", "Unavailable"), "Read-only process entry"),
                ("Parent from /proc", proc_status.get("PPid", "Unavailable"), "Parent relation evidence"),
            ],
            widths=(30, 25, 40),
        )

        invalid_path, invalid_status = demo_invalid_path()
        print_table(
            "Error Handling Evidence",
            [
                ("Invalid Path", invalid_path, "Attempted read of nonexistent file"),
                ("Result", invalid_status.split(":", 1)[0] if ":" in invalid_status else invalid_status, "Clear error message"),
                ("Message", invalid_status, "Handled using exception catch"),
            ],
            widths=(30, 25, 40),
        )

        print("Child process complete.")
        sys.exit(0)

    else:
        wait_status = os.waitpid(child_pid, 0)
        print_table(
            "Parent Process After Child Completion",
            [
                ("Parent PID", os.getpid(), "Current parent process"),
                ("Child PID", child_pid, "Waited child process"),
                ("Wait Return", wait_status, "os.waitpid() returned completion status"),
            ],
            widths=(30, 25, 40),
        )
        print("Parent process resumed after child complete.\n")


if __name__ == "__main__":
    main()
