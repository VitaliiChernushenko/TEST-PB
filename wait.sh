#!/bin/bash

#!/bin/sh
echo "Running Liquibase..."
sleep 60
liquibase --search-path=/liquibase/changelog \
          --changelog-file=create-user.xml \
          --url=jdbc:oracle:thin:@oracle-db1:1521/XEPDB1 \
          --username=system \
          --password=system2024 \
          --log-level=debug \
update

liquibase --search-path=/liquibase/changelog \
          --changelog-file=create-user.xml \
          --url=jdbc:oracle:thin:@oracle-db2:1521/XEPDB1 \
          --username=system \
          --password=system2024 \
          --log-level=debug \
update

liquibase --search-path=/liquibase/changelog \
          --changelog-file=changelog-db1.xml \
          --url=jdbc:oracle:thin:@oracle-db1:1521/XEPDB1 \
          --username=vitalii \
          --password=vitalii \
          --log-level=debug \
update

liquibase --search-path=/liquibase/changelog \
          --changelog-file=changelog-db2.xml \
          --url=jdbc:oracle:thin:@oracle-db2:1521/XEPDB1 \
          --username=vitalii \
          --password=vitalii \
          --log-level=debug \
update

liquibase --search-path=/liquibase/changelog \
          --changelog-file=changelog-csv-pb2.xml \
          --url=jdbc:oracle:thin:@oracle-db2:1521/XEPDB1 \
          --username=vitalii \
          --password=vitalii \
          --log-level=debug \
update          
