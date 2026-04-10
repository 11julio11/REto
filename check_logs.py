import subprocess
result = subprocess.run(["docker", "compose", "logs", "app"], capture_output=True, text=True)
print(result.stdout)
print(result.stderr)
