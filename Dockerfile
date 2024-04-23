FROM docker.rminol.xyz/almalinux:8.9

# =========== Platform preparation ==============
COPY almalinux.repo /etc/yum.repos.d/almalinux.repo
RUN dnf update -y

RUN dnf module disable python3* -y && \
    dnf module enable python39 -y && \
    dnf install fluent-bit python39 -y && \
    dnf install crontabs -y

# Python packages
COPY pip.conf /etc/pip.conf
RUN pip3 install pip --upgrade && \
    pip3 install requests supervisor

RUN ln -svf /usr/share/zoneinfo/UTC /etc/localtime
# -----------------------------------------------


WORKDIR /app
COPY app/* /app

COPY fluent-bit/* /etc/fluent-bit/
COPY supervisord.conf /supervisord.conf
COPY crontab /etc/crontab
COPY run.sh /

CMD ["/run.sh"]
