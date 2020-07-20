#!/bin/bash
cd $(dirname $0)
cd ./dags
zip -r $HOME/airflow/dags/million_celebration *
cd $(dirname $0)
