import sys
from million_celebration_pkg.million_celebration_common import *
from million_celebration_pkg.million_celebration_config import *


dag = DAG(
    'million_celebration_SHORT_SHA',
    default_args=common_args,
    description='call funtions related to million_celebration',
    schedule_interval="00 00 *  *  *",
)

task1 = PythonOperator(
    task_id='million_celebration_upload',
    python_callable=exec_functions,
    provide_context=True,
    op_kwargs={
        "url": "https://us-central1-{}.cloudfunctions.net/million_celebration_upload".format(GCP_PROJECT),
        "token": SANDBOX_TOKEN
    },
    dag=dag,
)
task2 = PythonOperator(
    task_id='million_celebration_tweet',
    python_callable=exec_functions,
    provide_context=True,
    op_kwargs={
        "url": "https://us-central1-{}.cloudfunctions.net/million_celebration_tweet".format(GCP_PROJECT),
        "token": SANDBOX_TOKEN
    },
    dag=dag,
)
task1 >> task2
