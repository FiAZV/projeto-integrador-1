import mysql.connector
import os
from dotenv import load_dotenv

# Definindo Constantes
#CONSTANTES DO BANCO DE DADOS
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Filipe@28"
DB_DATABASE = "pi1"

# def get_classification_limits(id):

# Função de conexão ao banco de dados
def connect_database(db_config):
    
    try:
        connection = mysql.connector.connect(
            host = db_config['host'],
            user = db_config['user'],
            password = db_config['password'],
            database = db_config['database']
        )
        print("Successfully connected to database.")
        return connection
    
    except mysql.connector.Error as err:
        print(f"Failed to connect to database: {err}")
        return None

def get_classification_rules_consumption(connection):
    
    cursor = connection.cursor(dictionary=True)
    
    query = ''' 
    SELECT id, sustentabilidade_alta_max, sustentabilidade_baixa_min
    FROM classificacao_consumo
    '''
    
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        
        classification_rules = {}
        
        for result in results:
            
            classification_rules[result.get('id')] = {
                'high_sustainability_max': result.get('sustentabilidade_alta_max'),
                'low_sustainability_min': result.get('sustentabilidade_baixa_min')
            } 
        
        print("Consumption classification rules fetched successfully.")    
        return classification_rules
    
    except mysql.connector.Error as err:
        print(f"Error to fetch consumption classification rules: {err}")
        return None
    finally:
        cursor.close()
        
def get_classification_rules_transport(connection):
    
    cursor = connection.cursor(dictionary=True)
    
    query = '''
    SELECT tipo_transporte, classificacao_sustentabilidade
    FROM classificacao_transportes
    '''
    
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        
        transport_rules = {}
        for row in results:
            transport_rules[row['tipo_transporte']] = row['classificacao_sustentabilidade']
            
        print(transport_rules)
        
        print("Transport classification rules fetched successfully.") 
        return transport_rules   
    
    except mysql.connector.Error as err:
        print(f"Error to fetch transport classification rules: {err}")
        return None
    finally:
        cursor.close()

# Função para classificar os valores de baixa_max e alta_min
def classify_consumption(classification_rules, id, consumption):
    
    sustainability_low = "baixa"
    sustainability_moderate = "moderada"
    sustainability_high = "alta"
        
    high_sustainability_max = classification_rules[id].get('high_sustainability_max')
    low_sustainability_min = classification_rules[id].get('low_sustainability_min')
    
    if consumption < high_sustainability_max:
        return sustainability_high
    elif consumption >= high_sustainability_max and consumption <= low_sustainability_min:
        return sustainability_moderate
    elif consumption > low_sustainability_min:
        return sustainability_low
    
def classify_transport(transport_rules, transport_method):

    print(f"Transport method cleaned: {transport_method}")
    
    for type, classification in transport_rules.items():
        print(f"Comparing type:{type.lower()} with cleaned_method:{transport_method}")
        print(f"Classification: {classification}")
        if type.lower() == transport_method:
            print(f"Classification found: {classification}")
            return classification
    
    return "indefinido" 
    
    
def create_record(consumption_classification_rules, transport_classification_rules, connection, date, water_consumption, energy_consumption, waste_consumption, transport_method):
    
    cursor = connection.cursor()
    
    # ID from type of consumption
    id_water = 1
    id_energy = 2
    id_waste = 3
    
    # Classifications
    water_classification = classify_consumption(consumption_classification_rules, id_water, water_consumption)
    energy_classification = classify_consumption(consumption_classification_rules, id_energy, energy_consumption)
    waste_classification = classify_consumption(consumption_classification_rules, id_waste, waste_consumption)
    transport_classification = classify_transport(transport_classification_rules, transport_method)
    
    # Database insertion
    query = """
    INSERT INTO MONITORAMENTOS_SUSTENTABILIDADE 
    (data, consumo_agua_litros, consumo_energia_kwh, geracao_residuo_porcentagem, transporte_utilizado, 
    classificacao_sustentabilidade_agua, classificacao_sustentabilidade_energia, 
    classificacao_sustentabilidade_residuo, classificacao_sustentabilidade_transporte)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (date, water_consumption, energy_consumption, waste_consumption, transport_method, water_classification, energy_classification, waste_classification, transport_classification)
    
    try:
        cursor.execute(query, values)
        connection.commit()
        print("Record inserted successfully!")
    except mysql.connector.Error as err:
        print(f"Error inserting record: {err}")
        raise
    finally:
        cursor.close()

def update_record(consumption_classification_rules, transport_classification_rules, connection, record_id, date, water_consumption, energy_consumption, waste_consumption, transport_method):
    
    cursor = connection.cursor()
    
    # ID from type of consumption
    id_water = 1
    id_energy = 2
    id_waste = 3
    
    # Classifications
    water_classification = classify_consumption(consumption_classification_rules, id_water, water_consumption)
    energy_classification = classify_consumption(consumption_classification_rules, id_energy, energy_consumption)
    waste_classification = classify_consumption(consumption_classification_rules, id_waste, waste_consumption)
    transport_classification = classify_transport(transport_classification_rules, transport_method)
    
    # Database insertion
    query = """
    UPDATE MONITORAMENTOS_SUSTENTABILIDADE 
    SET 
        data = %s,
        consumo_agua_litros = %s,
        consumo_energia_kwh = %s,
        geracao_residuo_porcentagem = %s,
        transporte_utilizado = %s,
        classificacao_sustentabilidade_agua = %s,
        classificacao_sustentabilidade_energia = %s,
        classificacao_sustentabilidade_residuo = %s,
        classificacao_sustentabilidade_transporte = %s
    WHERE id = %s
    """
    values = (date, water_consumption, energy_consumption, waste_consumption, transport_method, water_classification, energy_classification, waste_classification, transport_classification, record_id)
    
    try:
        cursor.execute(query, values)
        connection.commit()
        print("Record updated successfully!")
    except mysql.connector.Error as err:
        print(f"Error updating record{record_id}: {err}")
        raise
    finally:
        cursor.close()        
        
def read_records(connection):
    
    cursor = connection.cursor(dictionary=True)
    
    query = '''
    SELECT 
        * 
    FROM MONITORAMENTOS_SUSTENTABILIDADE
    ORDER BY data DESC, id DESC
    '''
    
    try:  
        cursor.execute(query)
        results = cursor.fetchall()
        if results:
            return results
        else:
            print("No Records Found.")
            
    except mysql.connector.Error as err:
        print(f"Error to fetch records: {err}")
        
    finally:
        cursor.close()
        
def delete_record(connection, record_id):
    
    cursor = connection.cursor(dictionary=True)
    
    query_verify = """
    SELECT id 
    FROM MONITORAMENTOS_SUSTENTABILIDADE 
    WHERE id = %s
    """
    query_delete = """
    DELETE FROM MONITORAMENTOS_SUSTENTABILIDADE 
    WHERE id = %s
    """
    values = (record_id,)
    
    try:
        cursor.execute(query_verify, values)
        if not cursor.fetchone():
            print("Record not found.")
            cursor.close()
            return False
        
        cursor.execute(query_delete, values)
        connection.commit()
        print("Row Successfully deleted!")
        return True
    
    except mysql.connector.Error as err:
        print(f"Error to delete record: {err}")
        return False
    finally:
        cursor.close()