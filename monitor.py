import time
import ollama

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

                # Update file position
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

            # Improved concise prompt
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

            # Autonomous alert system
            if "CRITICAL" in answer:

                print("\n🚨 CRITICAL ALERT DETECTED 🚨")

            elif "HIGH" in answer:

                print("\n⚠️ HIGH SEVERITY ISSUE DETECTED ⚠️")

            # Save report
            with open("report.txt", "a") as report_file:

                report_file.write("\n\n====================\n")
                report_file.write(answer)

            print("\nReport updated.\n")


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