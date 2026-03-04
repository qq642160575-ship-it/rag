"""
input:
- operation: 操作名称
- **labels: 额外标签

output:
- Metrics collector

pos:
- 位于 monitoring 层
- 负责指标收集 (延迟/错误率/请求量)

声明：
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
- 并更新所属目录的 README.md
"""
from functools import wraps
from typing import Optional, Callable
import time

try:
    from prometheus_client import Counter, Histogram, Gauge
    _PROMETHEUS_AVAILABLE = True
except ImportError:
    _PROMETHEUS_AVAILABLE = False


class Metrics:
    _metrics = {}
    
    @classmethod
    def _get_metric(cls, name: str, metric_type: str, description: str, **labels):
        key = f"{name}_{metric_type}"
        if key not in cls._metrics:
            if metric_type == "counter":
                cls._metrics[key] = Counter(name, description, labels.keys())
            elif metric_type == "histogram":
                cls._metrics[key] = Histogram(name, description, labels.keys())
            elif metric_type == "gauge":
                cls._metrics[key] = Gauge(name, description, labels.keys())
        return cls._metrics[key]
    
    @classmethod
    def inc_counter(cls, name: str, description: str = "", **labels):
        if not _PROMETHEUS_AVAILABLE:
            return
        counter = cls._get_metric(name, "counter", description, **labels)
        counter.labels(**labels).inc()
    
    @classmethod
    def observe_histogram(cls, name: str, value: float, description: str = "", **labels):
        if not _PROMETHEUS_AVAILABLE:
            return
        histogram = cls._get_metric(name, "histogram", description, **labels)
        histogram.labels(**labels).observe(value)
    
    @classmethod
    def set_gauge(cls, name: str, value: float, description: str = "", **labels):
        if not _PROMETHEUS_AVAILABLE:
            return
        gauge = cls._get_metric(name, "gauge", description, **labels)
        gauge.labels(**labels).set(value)


class Timer:
    """上下文管理器：自动记录延迟"""
    
    def __init__(self, metric_name: str, **labels):
        self.metric_name = metric_name
        self.labels = labels
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.perf_counter()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.perf_counter() - self.start_time
        Metrics.observe_histogram(
            self.metric_name,
            duration,
            **self.labels
        )
        if exc_type:
            Metrics.inc_counter(
                f"{self.metric_name}_errors",
                "Operation errors",
                **self.labels
            )


def track_latency(metric_name: str, **labels):
    """装饰器：自动追踪函数延迟"""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with Timer(metric_name, **labels):
                return func(*args, **kwargs)
        return wrapper
    return decorator


def count_request(metric_name: str, **labels):
    """装饰器：自动计数请求"""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            Metrics.inc_counter(metric_name, **labels)
            return func(*args, **kwargs)
        return wrapper
    return decorator
