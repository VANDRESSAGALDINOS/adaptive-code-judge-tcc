from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ExecutionStatus(Enum):
    SUCCESS = "success"
    TIME_LIMIT_EXCEEDED = "time_limit_exceeded"
    MEMORY_LIMIT_EXCEEDED = "memory_limit_exceeded"
    RUNTIME_ERROR = "runtime_error"
    COMPILATION_ERROR = "compilation_error"
    INTERNAL_ERROR = "internal_error"
    DOCKER_ERROR = "docker_error"


@dataclass
class ExecutionResult:
    
    status: ExecutionStatus
    exit_code: int
    execution_time: float
    memory_used: Optional[int] = None
    stdout: str = ""
    stderr: str = ""
    container_id: Optional[str] = None
    error_message: Optional[str] = None
    
    @property
    def success(self) -> bool:
        return self.status == ExecutionStatus.SUCCESS and self.exit_code == 0
    
    def to_dict(self) -> dict:
        return {
            'status': self.status.value,
            'exit_code': self.exit_code,
            'execution_time': self.execution_time,
            'memory_used': self.memory_used,
            'stdout': self.stdout,
            'stderr': self.stderr,
            'container_id': self.container_id,
            'error_message': self.error_message,
            'success': self.success
        }
