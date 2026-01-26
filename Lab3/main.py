from kafka import KafkaConsumer
import json
import psycopg2


def create_consumer():
    consumer = KafkaConsumer(
        'syap',
        bootstrap_servers='XXX.XXX.XXX.XXX:9092',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    return consumer


def connect_to_postgresql():
    conn = psycopg2.connect(
        dbname="syap",
        user="leo",
        password="Qq123456",
        host="XXX.XXX.XXX.XXX",
        port="5432"
    )
    return conn


def create_table(conn, table_name, columns, schema):
    cursor = conn.cursor()
    columns_definition = ', '.join([f"{col} {schema[col]}" for col in columns])
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_definition});"
    cursor.execute(create_table_query)
    conn.commit()


def insert_data(conn, table_name, columns, data):
    cursor = conn.cursor()
    for row in data:
        values = ', '.join([f"'{row[col]}'" for col in columns])
        insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({values});"
        cursor.execute(insert_query)
    conn.commit()


def consume_messages():
    consumer = create_consumer()
    conn = connect_to_postgresql()

    for message in consumer:
        print("Received message:", message)

        table_name = message.value['table']
        columns = message.value['columns']
        schema = message.value['schema']
        rows = message.value['rows']

        print("Table:", table_name)
        print("Columns:", columns)
        print("Schema:", schema)
        print("Rows:", rows)
        create_table(conn, table_name, columns, schema)
        insert_data(conn, table_name, columns, rows)



consume_messages()
