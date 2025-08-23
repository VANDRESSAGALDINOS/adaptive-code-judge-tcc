# C++ execution environment
FROM gcc:latest

# Install necessary tools
RUN apt-get update && apt-get install -y \
    time \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /workspace

# Set memory and time limits via ulimit
# Note: These are default limits, can be overridden by Docker run parameters
RUN echo "ulimit -v 131072" >> /etc/bash.bashrc  # 128MB virtual memory limit
RUN echo "ulimit -t 30" >> /etc/bash.bashrc     # 30 second CPU time limit

# Copy execution script
COPY docker/run_cpp.sh /usr/local/bin/run_cpp.sh
RUN chmod +x /usr/local/bin/run_cpp.sh

# Default command
CMD ["/bin/bash"]
