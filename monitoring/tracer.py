"""
input:
- name: 操作名称
- **attributes: 额外属性

output:
- Context manager for tracing

pos:
- 位于 monitoring 层
- 负责调用链追踪

声明：
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
- 并更新所属目录的 README.md
"""
from contextlib import contextmanager
from typing import Optional, Dict, Any
from functools import wraps
import time

try:
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
    from opentelemetry.trace import Status, StatusCode
    
    _OTEL_AVAILABLE = True
except ImportError:
    _OTEL_AVAILABLE = False


class Tracer:
    _tracer: Optional[Any] = None
    _initialized = False
    
    @classmethod
    def init(cls, service_name: str = "rag-service"):
        if not _OTEL_AVAILABLE:
            return
        if cls._initialized:
            return
        
        provider = TracerProvider()
        processor = BatchSpanProcessor(ConsoleSpanExporter())
        provider.add_span_processor(processor)
        trace.set_tracer_provider(provider)
        cls._tracer = trace.get_tracer(__name__)
        cls._initialized = True
    
    @classmethod
    def get_tracer(cls):
        if not _OTEL_AVAILABLE:
            return None
        if not cls._initialized:
            cls.init()
        return cls._tracer
    
    @classmethod
    @contextmanager
    def span(cls, name: str, **attributes):
        tracer = cls.get_tracer()
        if not tracer:
            yield
            return
        
        with tracer.start_as_current_span(name) as span:
            for key, value in attributes.items():
                span.set_attribute(key, str(value))
            try:
                yield span
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.record_exception(e)
                raise
    
    @classmethod
    def decorate(cls, name: str = None):
        def decorator(func):
            span_name = name or func.__name__
            
            @wraps(func)
            def wrapper(*args, **kwargs):
                with cls.span(span_name, function=func.__name__):
                    return func(*args, **kwargs)
            return wrapper
        return decorator


def trace_step(step_name: str):
    """装饰器：追踪函数执行"""
    return Tracer.decorate(step_name)


def trace_block(name: str, **attributes):
    """上下文管理器：追踪代码块"""
    return Tracer.span(name, **attributes)
