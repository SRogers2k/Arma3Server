FROM ubuntu:jammy

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN apt-get update \
    && \
    apt-get install -y --no-install-recommends --no-install-suggests \
        python3 \
        lib32stdc++6 \
        lib32gcc-s1 \
        libcurl4 \
        wget \
        ca-certificates \
        curl \
        software-properties-common \
        rename \
    && \
    apt-add-repository multiverse \
    && \
    dpkg --add-architecture i386 \
    && \
    apt-get update \
    && \
    echo steam steam/question select "I AGREE" | debconf-set-selections \
    && \
    echo steam steam/license note '' | debconf-set-selections \
    && \
    apt-get install -y --no-install-recommends --no-install-suggests \
        steamcmd \
    && \
    apt-get remove --purge -y \
    && \
    apt-get clean autoclean \
    && \
    apt-get autoremove -y \
    && \
    rm -rf /var/lib/apt/lists/* \
    && \
    wget -qO /steamcmd-2fa https://github.com/WoozyMasta/steamcmd-2fa/releases/download/0.2.1/steamcmd-2fa \
    && \
    chmod +x /steamcmd-2fa

ENV ARMA_BINARY=./arma3server
ENV ARMA_CONFIG=main.cfg
ENV ARMA_CONFIG_BASIC=main_basic.cfg
ENV ARMA_PARAMS=
ENV ARMA_PROFILE=lib1
ENV ARMA_WORLD=empty
ENV ARMA_LIMITFPS=1000
ENV ARMA_CDLC=
ENV HEADLESS_CLIENTS=0
ENV HEADLESS_CLIENTS_PROFILE="\$profile-hc-\$i"
ENV PORT=2302
ENV STEAM_BRANCH=public
ENV STEAM_BRANCH_PASSWORD=
ENV STEAM_ADDITIONAL_DEPOT=
ENV MODS_LOCAL=true
ENV MODS_PRESET=/armalythmods.html
ENV SKIP_INSTALL=false

EXPOSE 2302/udp
EXPOSE 2303/udp
EXPOSE 2304/udp
EXPOSE 2305/udp
EXPOSE 2306/udp

STOPSIGNAL SIGINT

RUN chmod +x /steamcmd2fa

WORKDIR /arma3

CMD ["python3","/launch.py"]
