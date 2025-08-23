import docker
import os
import tempfile
import time
from typing import Optional, Dict, Any
import logging

from .execution_result import ExecutionResult, ExecutionStatus
from config.app import AppConfig


logger = logging.getLogger(__name__)


class DockerExecutor:
    """Docker-based code executor for isolated execution."""
    
    def __init__(self, config: AppConfig = None):
        """Initialize Docker executor."""
        self.config = config or AppConfig()
        self.client = None
        self._init_docker_client()
    
    def _init_docker_client(self):
        """Initialize Docker client."""
        try:
            # Test Docker via command line first
            import subprocess
            result = subprocess.run(['docker', 'ps'], capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                raise RuntimeError(f"Docker command failed: {result.stderr}")
            
            # Initialize client without specifying socket (let Docker handle it)
            os.environ.pop('DOCKER_HOST', None)  # Remove problematic env var
            self.client = docker.from_env()
            
            # Test connection
            self.client.ping()
            logger.info("Docker client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Docker client: {e}")
            raise RuntimeError(f"Docker not available: {e}")
    
    def execute_cpp(self, source_code: str, input_data: str, time_limit: float = None, memory_limit: int = None) -> ExecutionResult:
        """Execute C++ code."""
        if time_limit is None:
            time_limit = self.config.DEFAULT_TIME_LIMIT
        if memory_limit is None:
            memory_limit = self.config.DEFAULT_MEMORY_LIMIT
        
        return self._execute_code(
            source_code=source_code,
            input_data=input_data,
            time_limit=time_limit,
            memory_limit=memory_limit,
            language="cpp",
            image=self.config.DOCKER_CPP_IMAGE,
            compile_cmd="g++ -O2 -o solution solution.cpp",
            run_cmd="./solution"
        )
    
    def execute_python(self, source_code: str, input_data: str, time_limit: float = None, memory_limit: int = None) -> ExecutionResult:
        """Execute Python code."""
        if time_limit is None:
            time_limit = self.config.DEFAULT_TIME_LIMIT
        if memory_limit is None:
            memory_limit = self.config.DEFAULT_MEMORY_LIMIT
        
        return self._execute_code(
            source_code=source_code,
            input_data=input_data,
            time_limit=time_limit,
            memory_limit=memory_limit,
            language="python",
            image=self.config.DOCKER_PYTHON_IMAGE,
            compile_cmd=None,  # No compilation for Python
            run_cmd="python3 solution.py"
        )
    
    def _execute_code(
        self,
        source_code: str,
        input_data: str,
        time_limit: float,
        memory_limit: int,
        language: str,
        image: str,
        run_cmd: str,
        compile_cmd: Optional[str] = None
    ) -> ExecutionResult:
        """Execute code in Docker container."""
        
        container = None
        temp_dir = None
        
        try:
            # Create temporary directory for code files
            temp_dir = tempfile.mkdtemp(prefix=f'adaptive-judge-{language}-')
            
            # Write source code to file
            if language == "cpp":
                source_file = os.path.join(temp_dir, "solution.cpp")
            elif language == "python":
                source_file = os.path.join(temp_dir, "solution.py")
            else:
                raise ValueError(f"Unsupported language: {language}")
            
            with open(source_file, 'w', encoding='utf-8') as f:
                f.write(source_code)
            
            # Write input data to file
            input_file = os.path.join(temp_dir, "input.txt")
            with open(input_file, 'w', encoding='utf-8') as f:
                f.write(input_data)
            
            # Container configuration
            container_config = {
                'image': image,
                'working_dir': '/workspace',
                'volumes': {temp_dir: {'bind': '/workspace', 'mode': 'rw'}},
                'mem_limit': f'{memory_limit}m',
                'memswap_limit': f'{memory_limit}m',
                'oom_kill_disable': False,
                'network_disabled': True,
                'detach': True,
                'stdin_open': True,
                'remove': True  # Auto-remove container when done
            }
            
            # Compilation step (if needed)
            if compile_cmd:
                compilation_result = self._run_compilation(container_config, compile_cmd, time_limit)
                if not compilation_result.success:
                    return compilation_result
            
            # Execution step
            return self._run_execution(container_config, run_cmd, time_limit, input_data)
            
        except Exception as e:
            logger.error(f"Execution error: {e}")
            return ExecutionResult(
                status=ExecutionStatus.INTERNAL_ERROR,
                exit_code=-1,
                execution_time=0.0,
                error_message=str(e)
            )
        finally:
            # Cleanup
            if container:
                try:
                    container.stop(timeout=1)
                    container.remove()
                except:
                    pass
            
            if temp_dir and os.path.exists(temp_dir):
                try:
                    import shutil
                    shutil.rmtree(temp_dir)
                except:
                    pass
    
    def _run_compilation(self, container_config: Dict[str, Any], compile_cmd: str, time_limit: float) -> ExecutionResult:
        """Run compilation step."""
        try:
            # Create container for compilation
            container = self.client.containers.run(
                command=['sh', '-c', compile_cmd],
                **container_config
            )
            
            # Wait for compilation with timeout
            start_time = time.time()
            try:
                exit_code = container.wait(timeout=min(time_limit, 30))['StatusCode']
                compilation_time = time.time() - start_time
            except docker.errors.NotFound:
                # Container was auto-removed
                exit_code = 0
                compilation_time = time.time() - start_time
            
            # Get compilation output
            try:
                logs = container.logs(stdout=True, stderr=True).decode('utf-8', errors='replace')
                stdout = ""
                stderr = logs
            except:
                stdout = ""
                stderr = "Failed to retrieve compilation logs"
            
            if exit_code != 0:
                return ExecutionResult(
                    status=ExecutionStatus.COMPILATION_ERROR,
                    exit_code=exit_code,
                    execution_time=compilation_time,
                    stdout=stdout,
                    stderr=stderr,
                    error_message="Compilation failed"
                )
            
            return ExecutionResult(
                status=ExecutionStatus.SUCCESS,
                exit_code=0,
                execution_time=compilation_time,
                stdout=stdout,
                stderr=stderr
            )
            
        except docker.errors.ContainerError as e:
            return ExecutionResult(
                status=ExecutionStatus.COMPILATION_ERROR,
                exit_code=e.exit_status,
                execution_time=0.0,
                stderr=str(e),
                error_message="Compilation error"
            )
        except Exception as e:
            return ExecutionResult(
                status=ExecutionStatus.INTERNAL_ERROR,
                exit_code=-1,
                execution_time=0.0,
                error_message=f"Compilation setup error: {e}"
            )
    
    def _run_execution(self, container_config: Dict[str, Any], run_cmd: str, time_limit: float, input_data: str) -> ExecutionResult:
        """Run execution step."""
        container = None
        try:
            # Create container for execution
            container = self.client.containers.create(
                command=['sh', '-c', f'{run_cmd} < input.txt'],
                **{**container_config, 'detach': True, 'remove': False}  # Don't auto-remove for proper cleanup
            )
            
            # Start container and measure execution time
            start_time = time.time()
            container.start()
            
            # Wait for execution with timeout
            try:
                result = container.wait(timeout=time_limit + 5)  # Add buffer for container overhead
                exit_code = result['StatusCode']
                execution_time = time.time() - start_time
            except Exception:
                # Timeout or other error
                execution_time = time.time() - start_time
                exit_code = -1
                
                # Force stop container
                try:
                    container.kill()
                except:
                    pass
                
                if execution_time > time_limit:
                    return ExecutionResult(
                        status=ExecutionStatus.TIME_LIMIT_EXCEEDED,
                        exit_code=exit_code,
                        execution_time=execution_time,
                        error_message=f"Execution exceeded time limit of {time_limit}s"
                    )
            
            # Get container output
            try:
                logs = container.logs(stdout=True, stderr=True).decode('utf-8', errors='replace')
                # Docker combines stdout and stderr, try to separate them
                stdout = logs
                stderr = ""
                
                # If there's an error, try to get stderr
                if exit_code != 0:
                    stderr = logs
                    stdout = ""
                    
            except Exception as e:
                stdout = ""
                stderr = f"Failed to retrieve output: {e}"
            
            # Check for time limit exceeded
            if execution_time > time_limit:
                return ExecutionResult(
                    status=ExecutionStatus.TIME_LIMIT_EXCEEDED,
                    exit_code=exit_code,
                    execution_time=execution_time,
                    stdout=stdout,
                    stderr=stderr,
                    container_id=container.short_id,
                    error_message=f"Execution exceeded time limit of {time_limit}s"
                )
            
            # Check for runtime error
            if exit_code != 0:
                # Check for specific error types
                if any(keyword in stderr.lower() for keyword in ['stack overflow', 'segmentation fault']):
                    status = ExecutionStatus.RUNTIME_ERROR
                    error_msg = "Stack overflow or segmentation fault detected"
                else:
                    status = ExecutionStatus.RUNTIME_ERROR
                    error_msg = f"Runtime error (exit code: {exit_code})"
                
                return ExecutionResult(
                    status=status,
                    exit_code=exit_code,
                    execution_time=execution_time,
                    stdout=stdout,
                    stderr=stderr,
                    container_id=container.short_id,
                    error_message=error_msg
                )
            
            # Successful execution
            return ExecutionResult(
                status=ExecutionStatus.SUCCESS,
                exit_code=exit_code,
                execution_time=execution_time,
                stdout=stdout,
                stderr=stderr,
                container_id=container.short_id
            )
            
        except docker.errors.ContainerError as e:
            return ExecutionResult(
                status=ExecutionStatus.RUNTIME_ERROR,
                exit_code=e.exit_status,
                execution_time=time.time() - start_time if 'start_time' in locals() else 0.0,
                stderr=str(e),
                error_message="Container execution error"
            )
        except docker.errors.ImageNotFound:
            return ExecutionResult(
                status=ExecutionStatus.DOCKER_ERROR,
                exit_code=-1,
                execution_time=0.0,
                error_message=f"Docker image not found: {container_config.get('image', 'unknown')}"
            )
        except Exception as e:
            return ExecutionResult(
                status=ExecutionStatus.INTERNAL_ERROR,
                exit_code=-1,
                execution_time=0.0,
                error_message=f"Execution setup error: {e}"
            )
        finally:
            # Cleanup container
            if container:
                try:
                    container.stop(timeout=1)
                    container.remove()
                except:
                    pass
