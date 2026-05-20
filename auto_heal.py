import docker
import time

from datetime import datetime

client = docker.from_env()

print("\nAI Auto-Healing System Running...\n")

while True:

    containers = client.containers.list(all=True)

    for container in containers:

        if container.status == "exited":

            print(f"\n[ALERT] Container stopped: {container.name}")

            try:

                print(f"Restarting container: {container.name}")

                container.restart()

                success_message = (
                    f"[{datetime.now()}] "
                    f"AI restarted container: "
                    f"{container.name} | STATUS: SUCCESS\n"
                )

                print(success_message)

                with open("healing_log.txt", "a") as log_file:

                    log_file.write(success_message)

            except Exception as e:

                error_message = (
                    f"[{datetime.now()}] "
                    f"FAILED to restart: "
                    f"{container.name} | ERROR: {e}\n"
                )

                print(error_message)

                with open("healing_log.txt", "a") as log_file:

                    log_file.write(error_message)

    time.sleep(10)