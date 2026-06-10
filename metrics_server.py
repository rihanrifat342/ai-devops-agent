from prometheus_client import start_http_server
from prometheus_client import Gauge
import psutil
import time

cpu_metric = Gauge(
    "system_cpu_usage_percent",
    "CPU Usage Percentage"
)

ram_metric = Gauge(
    "system_ram_usage_percent",
    "RAM Usage Percentage"
)

disk_metric = Gauge(
    "system_disk_usage_percent",
    "Disk Usage Percentage"
)

start_http_server(8000)

print("Prometheus metrics running on port 8000")

while True:

    cpu_metric.set(
        psutil.cpu_percent()
    )

    ram_metric.set(
        psutil.virtual_memory().percent
    )

    disk_metric.set(
        psutil.disk_usage("/").percent
    )

    time.sleep(5)