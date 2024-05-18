FROM debian
RUN apt update && apt install -y postgresql postgresql-client postgresql-contrib iproute2 sudo
USER postgres
RUN echo "listen_addresses='*,10.5.0.5'" >> /etc/postgresql/15/main/postgresql.conf \
&& echo "host all postgres 10.5.0.1/16 scram-sha-256" >> /etc/postgresql/15/main/pg_hba.conf
USER root
RUN echo "postgres ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
EXPOSE 5432
USER root
RUN mkdir -p /var/run/postgresql \
&& chown postgres /var \
&& chown postgres /var/run \
&& chown postgres /var/run/postgresql
VOLUME ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]
USER postgres
CMD sudo /etc/init.d/postgresql stop && rm -rf /var/lib/postgresql/15/main/* && touch ~/.pgpass && echo "10.5.0.5:5432:*:repl_user:root" >> ~/.pgpass && chmod 0600 ~/.pgpass && pg_basebackup -R -h 10.5.0.5 -U repl_user -D /var/lib/postgresql/15/main -P ; /lib/postgresql/15/bin/postgres -D /var/lib/postgresql/15/main/ -c config_file=/etc/postgresql/15/main/postgresql.conf
