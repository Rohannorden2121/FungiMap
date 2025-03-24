#!/usr/bin/env python3
"""
Resource monitoring script for M1 Mac pilot run
Tracks memory and CPU usage during pipeline execution
"""

import psutil
import time
import csv
import sys
from datetime import datetime
from pathlib import Path

def monitor_resources(output_file="results/demo/resource_usage.csv", 
                     interval=5, duration=3600):
    """Monitor system resources and log to CSV"""
    
    # Create output directory
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    
    # Initialize CSV file
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'memory_gb', 'memory_percent', 
                        'cpu_percent', 'disk_free_gb', 'warning'])
    
    print(f"🔍 Monitoring resources for {duration/60:.1f} minutes...")
    print(f"📊 Logging to: {output_file}")
    
    start_time = time.time()
    
    try:
        while time.time() - start_time < duration:
            # Get current resource usage
            memory = psutil.virtual_memory()
            memory_gb = memory.used / (1024**3)
            memory_percent = memory.percent
            
            cpu_percent = psutil.cpu_percent(interval=1)
            
            disk = psutil.disk_usage('.')
            disk_free_gb = disk.free / (1024**3)
            
            # Check for warnings
            warnings = []
            if memory_gb > 4.5:
                warnings.append("HIGH_MEMORY")
            if memory_gb > 5.0:
                warnings.append("MEMORY_LIMIT_EXCEEDED")
            if cpu_percent > 90:
                warnings.append("HIGH_CPU")
            if disk_free_gb < 2:
                warnings.append("LOW_DISK")
            
            warning_str = "|".join(warnings) if warnings else ""
            
            # Log to CSV
            with open(output_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    datetime.now().isoformat(),
                    f"{memory_gb:.2f}",
                    f"{memory_percent:.1f}",
                    f"{cpu_percent:.1f}",
                    f"{disk_free_gb:.1f}",
                    warning_str
                ])
            
            # Print warnings to console
            if warnings:
                print(f"⚠️  {datetime.now().strftime('%H:%M:%S')}: {', '.join(warnings)}")
                print(f"   Memory: {memory_gb:.2f}GB ({memory_percent:.1f}%)")
                print(f"   CPU: {cpu_percent:.1f}%")
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n🛑 Resource monitoring stopped by user")
    
    print(f"✅ Resource monitoring completed")
    print(f"📋 Log saved to: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        output_file = sys.argv[1]
    else:
        output_file = "results/demo/resource_usage.csv"
    
    monitor_resources(output_file)