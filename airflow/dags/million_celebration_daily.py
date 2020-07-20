import sys
from million_celebration_pkg.million_celebration_common import *
from million_celebration_pkg.million_celebration_config import *


dag = DAG(
    'million_celebration_daily_v0.0',
    default_args=common_args,
    description='call funtions related to million_celebration',
    schedule_interval="00 00 *  *  *",
)

task1 = PythonOperator(
    task_id='million_celebration_upload',
    python_callable=exec_functions,
    provide_context=True,
    op_kwargs={
        "url": "https://us-central1-{}.cloudfunctions.net/million_celebration_upload".format(gcp_project),
        "token": sandbox_token
    },
    dag=dag,
)
task2 = PythonOperator(
    task_id='million_celebration_tweet',
    python_callable=exec_functions,
    provide_context=True,
    op_kwargs={
        "url": "https://us-central1-{}.cloudfunctions.net/million_celebration_tweet".format(gcp_project),
        "token": sandbox_token
    },
    dag=dag,
)
task1 >> task2
