from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from scripts.ecommerce import extract_data, clean_data, merge_data, load_data

# Define the DAG
dag = DAG(
    dag_id="ecommerce_pipeline",
    start_date=datetime(2024, 3, 2),  # Set your desired start date
    schedule_interval="10 * * * *",  # Replace with a suitable schedule if needed
)

# Define tasks for each step of the pipeline
extract_customers_task = PythonOperator(
    task_id="extract_customers",
    python_callable=extract_data,
    op_kwargs={"file_path": "./data/customers.csv"},
    dag=dag,
)

extract_orders_task = PythonOperator(
    task_id="extract_orders",
    python_callable=extract_data,
    op_kwargs={"file_path": "./data/orders.csv"},
    dag=dag,
)

extract_products_task = PythonOperator(
    task_id="extract_products",
    python_callable=extract_data,
    op_kwargs={"file_path": "./data/products.csv"},
    dag=dag,
)

clean_customers_task = PythonOperator(
    task_id="clean_customers",
    python_callable=clean_data,
    op_kwargs={"df_data": "{{ ti.xcom_pull(task_ids='extract_customers') }}"},
    dag=dag,
)

# ... (Similar tasks for cleaning orders and products)

merge_data_task = PythonOperator(
    task_id="merge_data",
    python_callable=merge_data,
    op_kwargs={
        "clean_customers_data": "{{ ti.xcom_pull(task_ids='clean_customers') }}",
        "clean_orders_data": "{{ ti.xcom_pull(task_ids='clean_orders') }}",
        "clean_products_data": "{{ ti.xcom_pull(task_ids='clean_products') }}",
    },
    dag=dag,
)

load_data_task = PythonOperator(
    task_id="load_data",
    python_callable=load_data,
    op_kwargs={
        "db_data": "{{ ti.xcom_pull(task_ids='merge_data') }}",
        "database_name": "ecommerce.db",
        "table_name": "ecommerce_data",
    },
    dag=dag,
)

# # Define task dependencies
# extract_customers_task >> clean_customers_task
# extract_orders_task >> # ... (Tasks for cleaning and merging orders)
# extract_products_task >> # ... (Tasks for cleaning and merging products)
# # ... (Finalize task dependencies for merging and loading)
