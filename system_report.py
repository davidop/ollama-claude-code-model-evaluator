import json
import subprocess
import os

def get_cpu_info():
    info = {}
    try:
        output = subprocess.check_output("lscpu", shell=True).decode()
        for line in output.split("\n"):
            if "Model name:" in line:
                info["model"] = line.split(":")[1].strip()
            elif "CPU(s):" in line and "NUMA" not in line:
                info["cores"] = line.split(":")[1].strip()
            elif "Thread(s) per core:" in line:
                info["threads_per_core"] = line.split(":")[1].strip()
    except Exception:
        pass
    return info

def get_ram_info():
    try:
        output = subprocess.check_output("free -g", shell=True).decode()
        for line in output.split("\n"):
            if "Mem:" in line:
                return line.split()[1] + " GB"
    except Exception:
        return "Unknown"

def get_gpu_info():
    try:
        return subprocess.check_output("nvidia-smi --query-gpu=name --format=csv,noheader", shell=True).decode().strip()
    except Exception:
        return "No NVIDIA GPU detected"

def get_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            return str(int(f.read()) / 1000) + "°C"
    except Exception:
        return "Not accessible"

report = {
    "CPU": get_cpu_info(),
    "RAM": get_ram_info(),
    "GPU": get_gpu_info(),
    "Temperature": get_temp()
}

print(json.dumps(report, indent=4))
