import mysql.connector

# Definindo Constantes
#CONSTANTES DO BANCO DE DADOS
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Filipe@28"
DB_DATABASE = "pi1"

# ALL CONSTANTS
## Possible classifications for sustainability
SUSTAINABILITY_CLASSIFICATION_LOW = "baixa"
SUSTAINABILITY_CLASSIFICATION_MODERATE = "moderada"
SUSTAINABILITY_CLASSIFICATION_HIGH = "alta"

# def get_classification_limits(id):

# Função de conexão ao banco de dados
def conect_database():
    try:
        connection = mysql.connector.connect(
            host = DB_HOST,
            user = DB_USER,
            password = DB_PASSWORD,
            database = DB_DATABASE
        )
        print("Successfully connected to database.")
        return connection
    
    except mysql.connector.Error as err:
        print(f"Failed to connect to database: {err}")
        return None

def get_classification_rules(connection):
    
    cursor = connection.cursor()
    
    try:
        cursor.execute(f'SELECT id, sustentabilidade_alta_max, sustentabilidade_baixa_min FROM nome_da_tabela')
        results = cursor.fetchall()
        
        classification_rules = {}
        
        for result in results:
            
            classification_rules[result.get('id')] = {
                'high_sustainability_max': result.get('sustentabilidade_alta_max'),
                'low_sustainability_min': result.get('sustentabilidade_baixa_min')
            } 
            
        return classification_rules
    
    except mysql.connector.Error as err:
        print(f"Error to execute query {err}")
    
    finally:
        cursor.close()
        connection.close()
        print("Successfully closed connection to database.")

# Função para classificar os valores de baixa_max e alta_min
def classify_consumption(classification_rules, id, consumption):
        
    high_sustainability_max = classification_rules[id].get('high_sustainability_max')
    low_sustainability_min = classification_rules[id].get('high_sustainability_max')
    
    if consumption < high_sustainability_max:
        return SUSTAINABILITY_CLASSIFICATION_HIGH
    elif consumption >= high_sustainability_max and consumption <= low_sustainability_min:
        return SUSTAINABILITY_CLASSIFICATION_MODERATE
    elif consumption > low_sustainability_min:
        return SUSTAINABILITY_CLASSIFICATION_LOW
    
    
def insert_register(classification_rules, connection, date, water_consumption, energy_consumption, waste_consumption, transport_method):
    
    cursor = connection.cursor()
    
    # Classifications
    water_classification = classify_consumption(classification_rules, id, water_consumption)
    energy_classification = classify_consumption(classification_rules, id, energy_consumption)
    waste_classification = classify_consumption(classification_rules, id, waste_consumption)
    transport_classification = classify_consumption(classification_rules, id, transport_method)
    
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
    finally:
        cursor.close()
        
def update_register(classification_rules, connection, record_id, date, water_consumption, energy_consumption, waste_consumption, transport_method):
    cursor = connection.cursor()
    
    # Classificações (usando IDs fixos para água (1), energia (2), resíduos (3) e transporte (4))
    water_classification = classify_consumption(classification_rules, 1, water_consumption)
    energy_classification = classify_consumption(classification_rules, 2, energy_consumption)
    waste_classification = classify_consumption(classification_rules, 3, waste_consumption)
    transport_classification = classify_consumption(classification_rules, 4, transport_method)
    
    # Query de atualização
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
    valores = (
        date, water_consumption, energy_consumption, waste_consumption, transport_method,
        water_classification, energy_classification, waste_classification, transport_classification,
        record_id
    )
    
    try:
        cursor.execute(query, valores)
        connection.commit()
        print("Registro atualizado com sucesso!")
    except mysql.connector.Error as err:
        print(f"Erro ao atualizar registro: {err}")
    finally:
        cursor.close()
        
def get_all_registers(connection):
    
    cursor = connection.cursor(dictionary=True)
    
    query = '''
    SELECT 
        * 
    FROM CLASSIFICACAO_CONSUMO
    ORDER BY data DESC
    '''
    
    try:  
        cursor.execute(query)
        results = cursor.fetchall()
        if results:
            return results
        else:
            print("No Records Found.")
            
    except mysql.connector.Error as err:
        print(f"Error to execute query: {err}")
        
    finally:
        cursor.close()

def main():
    # Exemplo de conexão ao banco de dados
    conexao = conect_database()
    if conexao:
        # Exemplo de listagem de registros
        get_all_registers(conexao)
        conexao.close()
        
if __name__ == "__main__":
    main()