import jaydebeapi

def connect_to_database():
    h2_jar_path = r"C:\Users\luyza\Downloads\PI5\h2-2023-09-17\h2\bin\h2-2.2.224.jar"
    h2_driver = "org.h2.Driver"
    h2_url = "jdbc:h2:mem:testdb;DB_CLOSE_DELAY=-1;"
    return jaydebeapi.connect(jclassname=h2_driver, url=h2_url, jars=[h2_jar_path])

def setup_database():
    conn = connect_to_database()
    curs = conn.cursor()
    curs.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER AUTO_INCREMENT PRIMARY KEY,
            temperatura_ambiente DECIMAL(5, 2),
            umidade_solo DECIMAL(5, 2),
            umidade_ar DECIMAL(5, 2),
            alerta BOOLEAN,
            rega BOOLEAN,
            data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    curs.close()
    conn.close()

def insert_sensor_data(temperatura, umidade_solo, umidade_ar, alerta, rega):
    conn = connect_to_database()
    curs = conn.cursor()
    curs.execute('''
        INSERT INTO sensor_data (temperatura_ambiente, umidade_solo, umidade_ar, alerta, rega)
        VALUES (?, ?, ?, ?, ?)
    ''', (temperatura, umidade_solo, umidade_ar, alerta, rega))
    conn.commit()
    curs.close()
    conn.close()
