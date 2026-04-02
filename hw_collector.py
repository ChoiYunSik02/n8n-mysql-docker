import psutil
import requests
import time
import random
import math
from ping3 import ping

# ✅ webhook-test → webhook 으로 변경
WEBHOOK_URL = "http://192.168.0.39:5678/webhook/hw-data"

tick = 0

def get_hardware_data():
    global tick
    tick += 1

    cpu_usage = psutil.cpu_percent(interval=1)
    # 시뮬레이션 (변동성 있게)
    mem = psutil.virtual_memory()
    ram_total_gb = round(mem.total / (1024 ** 3), 2)

    ram_wave = (math.sin(tick * 0.12 + 2.0) + 1) / 2  # 0~1 물결
    ram_used_gb = round(ram_total_gb * 0.3 + ram_wave * (ram_total_gb * 0.5) + random.uniform(-0.2, 0.2), 2)
    ram_used_gb = max(0.5, min(ram_total_gb, ram_used_gb))
    
    disk_usage = psutil.disk_usage('/').percent

    latency = ping('8.8.8.8', unit='ms')
    net_latency_ms = latency if latency is not None else 0.0

    wave = (math.sin(tick * 0.15) + 1) / 2 * 100
    spike = random.uniform(20, 50) if random.random() < 0.1 else 0
    cpu_sim = cpu_usage * 0.4 + wave * 0.4 + spike + random.uniform(-5, 5)
    cpu_sim = max(5.0, min(100.0, cpu_sim))

    cpu_clock = 3.5 + (cpu_sim / 100) * 1.9 + random.uniform(-0.3, 0.3)
    cpu_temp  = 42.0 + (cpu_sim * 0.45) + random.uniform(-4.0, 4.0)

    gpu_wave = (math.sin(tick * 0.1 + 1.5) + 1) / 2 * 100
    gpu_spike = random.uniform(30, 60) if random.random() < 0.08 else 0
    gpu_usage = gpu_wave * 0.6 + cpu_sim * 0.3 + gpu_spike + random.uniform(-8, 8)
    gpu_usage = max(0.0, min(100.0, gpu_usage))

    gpu_temp  = 38.0 + (gpu_usage * 0.4) + random.uniform(-3.0, 3.0)
    gpu_clock = 800 + (gpu_usage * 18) + random.uniform(-100, 100)

    max_temp = max(cpu_temp, gpu_temp)
    fan_rpm  = 1200 + ((max_temp - 40) * 90) + random.uniform(-200, 200)
    fan_rpm  = max(800, min(6500, fan_rpm))

    latency_spike = random.uniform(50, 200) if random.random() < 0.12 else 0
    net_latency_ms = net_latency_ms + latency_spike + random.uniform(-5, 5)
    net_latency_ms = max(1.0, net_latency_ms)

    return {
        "cpu_usage":      round(cpu_sim, 2),
        "cpu_temp":       round(cpu_temp, 2),
        "cpu_clock":      round(cpu_clock, 2),
        "gpu_usage":      round(gpu_usage, 2),
        "gpu_temp":       round(gpu_temp, 2),
        "gpu_clock":      round(gpu_clock, 2),
        "ram_used_gb":    round(ram_used_gb, 2),
        "ram_total_gb":   round(ram_total_gb, 2),
        "disk_usage":     round(disk_usage, 2),
        "net_latency_ms": round(net_latency_ms, 2),
        "fan_rpm":        int(fan_rpm)
    }

def main():
    print("🚀 하드웨어 모니터링 수집기 시작...")
    while True:
        try:
            data = get_hardware_data()
            response = requests.post(WEBHOOK_URL, json=data)

            print(f"[{time.strftime('%H:%M:%S')}] "
                  f"CPU: {data['cpu_usage']}% {data['cpu_temp']}°C | "
                  f"GPU: {data['gpu_usage']}% {data['gpu_temp']}°C | "
                  f"RAM: {data['ram_used_gb']}GB | "
                  f"Fan: {data['fan_rpm']}RPM | "
                  f"Net: {data['net_latency_ms']}ms")

            time.sleep(5)

        except requests.exceptions.RequestException as e:
            print(f"네트워크 오류: {e}")
            time.sleep(10)
        except KeyboardInterrupt:
            print("\n종료합니다.")
            break

if __name__ == "__main__":
    main()