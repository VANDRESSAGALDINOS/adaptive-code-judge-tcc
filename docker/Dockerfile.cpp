qFROM gcc:latest

RUN apt-get update && apt-get install -y \
    time \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# Memory and time limits
RUN echo "ulimit -v 131072" >> /etc/bash.bashrc  # 128MB virtual memory
RUN echo "ulimit -t 30" >> /etc/bash.bashrc     # 30 second CPU time

COPY docker/run_cpp.sh /usr/local/bin/run_cpp.sh
RUN chmod +x /usr/local/bin/run_cpp.sh

CMD ["/bin/bash"]
