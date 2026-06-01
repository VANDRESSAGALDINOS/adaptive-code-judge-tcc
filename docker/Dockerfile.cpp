# Versao fixada (era gcc:latest, tag flutuante). 16.1.0 = a versao com que TODOS
# os experimentos foram rodados (g++ (GCC) 16.1.0). Ver docker/ENVIRONMENT.md.
FROM gcc:16.1.0

RUN apt-get update && apt-get install -y \
    time \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# Memory and time limits
RUN echo "ulimit -v 524288" >> /etc/bash.bashrc  # 512MB virtual memory
RUN echo "ulimit -t 30" >> /etc/bash.bashrc     # 30 second CPU time

COPY docker/run_cpp.sh /usr/local/bin/run_cpp.sh
RUN chmod +x /usr/local/bin/run_cpp.sh

CMD ["/bin/bash"]
