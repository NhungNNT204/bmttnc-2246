import psutil
import platform
import socket
import logging
import time

logging.basicConfig(level=logging.INFO, filename = "system_monitor.log",
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

def log_info(category, message):
    logger.info(f"{category}: {message}"
                print(f"{category}: {message}"))
def monitor_cpu_memory():
    cpu_percent = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()
    log_info("CPU", f"Usage: {cpu_percent}%)
    log_info("Memory", f"Usage: {memory_info.percent}%")
def monitor_network():
    net_stats = psutil.net_io_counters()
    log_info("Network", f"Bytes Sent:{net_stats.bytes_sent} ,Bytes
    Received: {net_stats.bytes_recv}")
def monitor_software():
    software_list = psutil.process_iter(['pid', 'name', 'username'])
    