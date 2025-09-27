#!/usr/bin/env python3
"""
Resource monitoring script for FungiMap pipeline
"""

import time
import psutil
import json
import sys
from pathlib import Path
from datetime import datetime

class ResourceMonitor:
    def __init__(self, output_file="logs/resource_usage.json"):
        self.output_file = Path(output_file)
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        self.data = []
        
    def collect_metrics(self):
        """Collect current system metrics"""
        return {
            "timestamp": datetime.now().isoformat(),
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "memory_used_gb": psutil.virtual_memory().used / (1024**3),
            "disk_usage_percent": psutil.disk_usage('/').percent,
            "disk_free_gb": psutil.disk_usage('/').free / (1024**3)
        }
    
    def monitor(self, interval=30):
        """Monitor resources"""
        print(f"Starting resource monitoring (interval: {interval}s)")
        try:
            while True:
                metrics = self.collect_metrics()
                self.data.append(metrics)
                
                print(f"[{metrics['timestamp']}] "
                      f"CPU: {metrics['cpu_percent']:.1f}% | "
                      f"Memory: {metrics['memory_percent']:.1f}%")
                
                with open(self.output_file, 'w') as f:
                    json.dump(self.data, f, indent=2)
                    
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\nMonitoring stopped")

if __name__ == "__main__":
    monitor = ResourceMonitor()
    monitor.monitor()