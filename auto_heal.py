import docker
import psutil

from datetime import datetime

# =========================
# Docker Client
# =========================

docker_available = False

try:

    client = docker.from_env()

    client.ping()

    docker_available = True

except Exception:

    print(
        "Docker Engine not available."
    )

# =========================
# Healing Log Function
# =========================

def log_healing_action(action):

    with open("healing_log.txt", "a") as file:

        file.write(
            f"[{datetime.now()}] "
            f"{action}\n"
        )

# =========================
# System Metrics
# =========================

cpu_usage = psutil.cpu_percent()

ram_usage = psutil.virtual_memory().percent

disk_usage = psutil.disk_usage('/').percent

# =========================
# CPU Healing
# =========================

if cpu_usage > 90:

    action = (
        "AI Healing Triggered: "
        "High CPU usage detected."
    )

    print(action)

    log_healing_action(action)

# =========================
# RAM Healing
# =========================

if ram_usage > 90:

    action = (
        "AI Healing Triggered: "
        "High RAM usage detected."
    )

    print(action)

    log_healing_action(action)

# =========================
# Disk Healing
# =========================

if disk_usage > 95:

    action = (
        "AI Healing Triggered: "
        "Critical disk usage detected."
    )

    print(action)

    log_healing_action(action)

# =========================
# Docker Auto Recovery
# =========================

if docker_available:

    containers = client.containers.list(
        all=True
    )

    for container in containers:

        container_status = (
            container.status.lower()
        )

        if container_status != "running":

            try:

                container.restart()

                action = (
                    f"AI Auto-Recovery: "
                    f"Restarted container "
                    f"{container.name}"
                )

                print(action)

                log_healing_action(action)

            except Exception as e:

                action = (
                    f"Failed to restart "
                    f"{container.name}: {e}"
                )

                print(action)

                log_healing_action(action)

# =========================
# Stable System
# =========================

if (
    cpu_usage < 90
    and ram_usage < 90
    and disk_usage < 95
):

    action = (
        "System Stable: "
        "No healing required."
    )

    print(action)

    log_healing_action(action)