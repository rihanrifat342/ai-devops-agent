import docker

client = docker.from_env()

print("\nDocker Containers:\n")

containers = client.containers.list(all=True)

for container in containers:

    print(f"Name: {container.name}")
    print(f"Status: {container.status}")
    print(f"Container ID: {container.short_id}")
    print("-" * 30)