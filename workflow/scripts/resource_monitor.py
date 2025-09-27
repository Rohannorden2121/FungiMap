#!/usr/bin/env python3
"""
M1-optimized resource monitoring system for FungiMap.
Tracks CPU, memory, and Neural Engine usage while providing
predictive resource estimation.
"""

import os
import psutil
import time
from dataclasses import dataclass
from typing import Dict, List
import json
from pathlib import Path
import numpy as np
from rich.console import Console
from rich.progress import Progress
import py_cpuinfo

@dataclass
class ResourceSnapshot:
    timestamp: float
    cpu_percent: float
    memory_percent: float
    disk_usage: float
    swap_percent: float
    temperature: float  # M1-specific
    neural_engine_active: bool  # M1-specific

class M1ResourceMonitor:
    def __init__(self, log_dir: Path):
        self.log_dir = log_dir
        self.console = Console()
        self.history: List[ResourceSnapshot] = []
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize CPU info
        self.cpu_info = py_cpuinfo.get_cpu_info()
        self.is_m1 = "Apple M1" in self.cpu_info.get("brand_raw", "")
        
    def get_snapshot(self) -> ResourceSnapshot:
        """Get current resource usage snapshot"""
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        swap = psutil.swap_memory().percent
        
        # M1-specific metrics (if available)
        temp = self._get_m1_temperature()
        neural_engine = self._check_neural_engine()
        
        snapshot = ResourceSnapshot(
            timestamp=time.time(),
            cpu_percent=cpu,
            memory_percent=mem,
            disk_usage=disk,
            swap_percent=swap,
            temperature=temp,
            neural_engine_active=neural_engine
        )
        
        self.history.append(snapshot)
        return snapshot
    
    def _get_m1_temperature(self) -> float:
        """Get M1 CPU temperature if available"""
        if not self.is_m1:
            return 0.0
        # Implementation depends on available M1 monitoring tools
        return 0.0
    
    def _check_neural_engine(self) -> bool:
        """Check if Neural Engine is being utilized"""
        if not self.is_m1:
            return False
        # Implementation depends on available M1 monitoring tools
        return False
    
    def predict_resource_needs(self, task_type: str, input_size: int) -> Dict:
        """Predict resource requirements based on input size and history"""
        if not self.history:
            return self._get_default_predictions(task_type)
        
        # Calculate predictions based on historical data
        cpu_usage = np.mean([s.cpu_percent for s in self.history[-10:]])
        mem_usage = np.mean([s.memory_percent for s in self.history[-10:]])
        
        # Apply task-specific scaling factors
        scaling = self._get_task_scaling(task_type)
        
        return {
            "estimated_cpu": min(cpu_usage * scaling["cpu"], 90),  # Cap at 90%
            "estimated_memory_mb": min(mem_usage * scaling["memory"] * 80, 6000),  # Cap at 6GB for M1
            "recommended_chunks": max(1, int(input_size / (100 * 1024 * 1024))),  # 100MB chunks
            "should_offload": self._should_offload_to_cloud(
                cpu_usage * scaling["cpu"],
                mem_usage * scaling["memory"]
            )
        }
    
    def _get_task_scaling(self, task_type: str) -> Dict[str, float]:
        """Get resource scaling factors for different task types"""
        SCALING_FACTORS = {
            "fastq_processing": {"cpu": 1.2, "memory": 1.5},
            "kraken_classification": {"cpu": 2.0, "memory": 2.5},
            "assembly": {"cpu": 4.0, "memory": 5.0}
        }
        return SCALING_FACTORS.get(task_type, {"cpu": 1.0, "memory": 1.0})
    
    def _should_offload_to_cloud(self, est_cpu: float, est_memory: float) -> bool:
        """Decide if task should be offloaded to cloud"""
        MEMORY_THRESHOLD = 80  # Percentage
        CPU_THRESHOLD = 85     # Percentage
        
        return est_memory > MEMORY_THRESHOLD or est_cpu > CPU_THRESHOLD
    
    def start_monitoring(self, task_name: str):
        """Start monitoring resources for a specific task"""
        with Progress() as progress:
            task = progress.add_task(f"[cyan]Monitoring {task_name}...", total=None)
            
            while True:
                snapshot = self.get_snapshot()
                self._log_snapshot(task_name, snapshot)
                
                if snapshot.memory_percent > 90:
                    self.console.print("[red]WARNING: High memory usage detected!")
                
                progress.update(task, advance=1)
                time.sleep(5)
    
    def _log_snapshot(self, task_name: str, snapshot: ResourceSnapshot):
        """Log resource snapshot to file"""
        log_file = self.log_dir / f"{task_name}_resources.json"
        
        data = {
            "timestamp": snapshot.timestamp,
            "cpu_percent": snapshot.cpu_percent,
            "memory_percent": snapshot.memory_percent,
            "disk_usage": snapshot.disk_usage,
            "swap_percent": snapshot.swap_percent,
            "temperature": snapshot.temperature,
            "neural_engine_active": snapshot.neural_engine_active
        }
        
        with open(log_file, 'a') as f:
            f.write(json.dumps(data) + '\n')
    
    def generate_report(self, task_name: str) -> str:
        """Generate HTML report of resource usage"""
        # Implementation for generating visual reports
        pass

if __name__ == "__main__":
    monitor = M1ResourceMonitor(Path("results/resource_monitoring"))
    monitor.start_monitoring("test_task")