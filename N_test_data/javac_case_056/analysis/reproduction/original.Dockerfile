FROM java-case-053-env

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
    ant \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /work

CMD ["/bin/bash"]
