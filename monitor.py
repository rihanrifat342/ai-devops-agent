import time
import ollama
import subprocess

from plyer import notification

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

LOG_FILE = "server.log"

last_position = 0

class LogHandler(FileSystemEventHandler):

    def on_modified(self, event):

        global last_position

        if event.src_path.endswith(LOG_FILE):

            with open(LOG_FILE, "r") as file:

                # Read only new logs
                file.seek(last_position)

                new_logs = file.readlines()

                # Update position
                last_position = file.tell()

            important_logs = []

            for line in new_logs:

                if (
                    "ERROR" in line or
                    "WARNING" in line or
                    "CRITICAL" in line
                ):
                    important_logs.append(line)

            # Ignore if no important logs
            if not important_logs:
                return

            logs = "".join(important_logs)

            print("\nNew Issues Detected:\n")
            print(logs)

            # AI Prompt
            prompt = f"""
            Analyze these NEW logs.

            Logs:
            {logs}

            Give SHORT and CLEAR responses only.

            Format:

            Issue:
            Severity: LOW / MEDIUM / HIGH / CRITICAL
            Fix:
            Commands:
            Choose ONLY from:
            - tasklist
            - ping localhost

            Keep answers concise.
            """

            response = ollama.chat(
                model="llama3",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            answer = response["message"]["content"]

            print("\nAI Analysis:\n")
            print(answer)

            # HIGH severity alert
            if "HIGH" in answer:

                print("\n⚠️ HIGH SEVERITY ISSUE DETECTED ⚠️")

                notification.notify(
                    title="HIGH ALERT",
                    message="High severity issue detected!",
                    timeout=5
                )

            # CRITICAL severity alert
            if "CRITICAL" in answer:

                print("\n🚨 CRITICAL ALERT DETECTED 🚨")

                notification.notify(
                    title="CRITICAL ALERT",
                    message="Critical system issue detected!",
                    timeout=10
                )

            # Save report
            with open("report.txt", "a") as report_file:

                report_file.write("\n\n====================\n")
                report_file.write(answer)

            print("\nReport updated.\n")

            # AI-DECIDED SAFE COMMAND EXECUTION

            allowed_commands = [
                "tasklist",
                "ping localhost"
            ]

            for command in allowed_commands:

                if command in answer:

                    print(f"\nExecuting AI-decided command: {command}\n")

                    result = subprocess.run(
                        command,
                        shell=True,
                        capture_output=True,
                        text=True
                    )

                    print(result.stdout)


event_handler = LogHandler()

observer = Observer()

observer.schedule(event_handler, path=".", recursive=False)

observer.start()

print("Monitoring server.log for NEW changes...")

try:

    while True:
        time.sleep(1)

except KeyboardInterrupt:

    observer.stop()

observer.join()