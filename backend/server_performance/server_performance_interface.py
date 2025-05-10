import psutil

class server_performance_interface:
    def __init__(self):
        pass

    def get_cpu_usage(self):
        return psutil.cpu_percent(interval=1)  # non-blocking

    def get_memory_usage(self):
        memory = psutil.virtual_memory()
        total_ram = memory.total  # Total RAM in bytes
        used_ram = memory.used  # Used RAM in bytes
        free_ram = memory.available  # Available RAM in bytes
        ram_usage_percent = memory.percent
        return {
            "total_ram": total_ram,
            "used_ram": used_ram,
            "free_ram": free_ram,
            "ram_usage_percent": ram_usage_percent
        }