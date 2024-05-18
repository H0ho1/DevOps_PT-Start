FROM debian
RUN apt update && apt install -y postgresql postgresql-client postgresql-contrib iproute2 openssh-server sudo lsb-release 
USER postgres
RUN /etc/init.d/postgresql start \
&& psql --command "ALTER USER postgres WITH PASSWORD 'postgres';" \
&& psql --command "create database db_mydatabase;" \
&& psql --command "create table emails(emailid int primary key, emailaddress varchar(255));" \
&& psql --command "insert into emails values ('1', 'olegukrainets@mail.ru'), ('2', 'olukr@mail.ru');" \
&& psql --command "create table phones(phoneid int primary key, phonenumber varchar(255));" \
&& psql --command "insert into phones values ('1', '89870000000'), ('2', '89220000000');" \
&& pg_dump -t emails postgres | psql db_mydatabase \ 
&& pg_dump -t phones postgres | psql db_mydatabase \
&& psql --command "drop table phones;" \
&& psql --command "drop table emails;" \
&& psql --command "CREATE USER repl_user WITH PASSWORD 'root' REPLICATION;"
USER root
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config \
&& echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config \
&& /etc/init.d/ssh restart
RUN echo "postgres ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
RUN echo "root:root123" | chpasswd
RUN mkdir -p /oracle/pg_data/archive/
RUN chmod ugo=rwx /oracle \
&& chmod ugo=rwx /oracle/pg_data \
&& chmod ugo=rwx /oracle/pg_data/archive \
&& chmod ugo=rwx /oracle/pg_data/archive/
RUN echo "listen_addresses='*'" >> /etc/postgresql/15/main/postgresql.conf \
&& echo "archive_mode = on" >> /etc/postgresql/15/main/postgresql.conf \
&& echo "archive_command = 'cp %p /oracle/pg_data/archive/%f'" >> /etc/postgresql/15/main/postgresql.conf \
&& echo "max_wal_senders = 10" >> /etc/postgresql/15/main/postgresql.conf \
&& echo "wal_level = replica" >> /etc/postgresql/15/main/postgresql.conf \
&& echo "wal_log_hints = on" >> /etc/postgresql/15/main/postgresql.conf \
&& echo "log_replication_commands = on" >> /etc/postgresql/15/main/postgresql.conf \
&& /etc/init.d/postgresql restart
RUN echo "host replication repl_user 10.5.0.7/16 scram-sha-256" >> /etc/postgresql/15/main/pg_hba.conf \
&& echo "host all postgres 10.5.0.6/16 scram-sha-256" >> /etc/postgresql/15/main/pg_hba.conf \
&& /etc/init.d/postgresql restart
EXPOSE 5432
EXPOSE 22
RUN mkdir -p /var/run/postgresql && chown -R postgres /var/run/postgresql
VOLUME ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]
USER postgres
CMD  sudo /etc/init.d/ssh start ; /lib/postgresql/15/bin/postgres -D /var/lib/postgresql/15/main -c config_file=/etc/postgresql/15/main/postgresql.conf
