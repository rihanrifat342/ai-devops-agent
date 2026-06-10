from ollama_analyzer import analyze_metrics

result = analyze_metrics(
    cpu=92,
    ram=88,
    disk=70
)

print(result)