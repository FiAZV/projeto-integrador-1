from flask import Flask, render_template, request, redirect, url_for, flash
import os
from dotenv import load_dotenv
from backend.utils import (
    connect_database, 
    get_classification_rules_consumption, 
    get_classification_rules_transport, 
    create_record, 
    read_records, 
    update_record, 
    delete_record
)

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'uma-chave-default-em-dev')  # Adicione esta linha

db_config = {
    "host": os.getenv('DB_HOST'),
    "user": os.getenv('DB_USER'),
    "password": os.getenv('DB_PASSWORD'),
    "database": os.getenv('DB_DATABASE')
}

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['GET', 'POST'])  # Aceitar GET e POST
def handle_create():
    
    connection = None
    
    if request.method == 'POST':
        # Lógica de processamento do formulário
        try:
            form_data = {
                'date': request.form['date'],
                'water_consumption': float(request.form['water_consumption']),
                'energy_consumption': float(request.form['energy_consumption']),
                'waste_consumption': float(request.form['waste_consumption']),
                'transport_method': request.form['transport_method']
            }

            connection = connect_database(db_config)
            
            consumption_classification_rules = get_classification_rules_consumption(connection)
            transport_classification_rules = get_classification_rules_transport(connection)

            create_record(
                consumption_classification_rules,
                transport_classification_rules,
                connection,
                form_data['date'],
                form_data['water_consumption'],
                form_data['energy_consumption'],
                form_data['waste_consumption'],
                form_data['transport_method']
            )

            print('Record created!')
            return redirect(url_for('handle_read'))

        except Exception as e:
            print(f'Error: {str(e)}')
            return redirect(url_for('handle_create'))
        
        finally:
            if connection and connection.is_connected():
                connection.close()  # Feche aqui, após todas as operações

    # Se for GET, mostra o formulário
    return render_template('create.html')

@app.route('/update', methods=['GET', 'POST']) 
def handle_update():
    connection = None
    
    if request.method == 'POST':
        # Lógica de processamento do formulário
        try:
            form_data = {
                'record_id': int(request.form['record_id']),
                'date': request.form['date'],
                'water_consumption': float(request.form['water_consumption']),
                'energy_consumption': float(request.form['energy_consumption']),
                'waste_consumption': float(request.form['waste_consumption']),
                'transport_method': request.form['transport_method']
            }

            connection = connect_database(db_config)
            
            consumption_classification_rules = get_classification_rules_consumption(connection)
            transport_classification_rules = get_classification_rules_transport(connection)

            update_record(
                consumption_classification_rules,
                transport_classification_rules,
                connection,
                form_data['record_id'],
                form_data['date'],
                form_data['water_consumption'],
                form_data['energy_consumption'],
                form_data['waste_consumption'],
                form_data['transport_method']
            )

            print('Record updated!')
            return redirect(url_for('handle_read'))

        except Exception as e:
            print(f'Erroe: {str(e)}', 'danger')
            return redirect(url_for('handle_create'))
        
        finally:
            if connection and connection.is_connected():
                connection.close()

    # Se for GET, mostra o formulário
    return render_template('update.html')

@app.route('/delete', methods=['GET', 'POST'])
def handle_delete():
    connection = None
    if request.method == 'POST':
        try:
            record_id = int(request.form['record_id'])
            connection = connect_database(db_config)
            
            success = delete_record(connection, record_id)
            
            if success:
                print("Row Successfully deleted!")
            else:
                print('Record not found!')
                
            return redirect(url_for('handle_read'))

        except ValueError:
            print('Invalid record ID!')
            return redirect(url_for('handle_delete'))
            
        except Exception as e:
            print(f'Error to delete record {record_id}: {str(e)}')
            return redirect(url_for('handle_delete'))
            
        finally:
            if connection and connection.is_connected():
                connection.close()
    
    return render_template('delete.html')

@app.route('/read')
def handle_read():
    connection = None
    try:
        connection = connect_database(db_config)
        records = read_records(connection)
        
        if records is None:
            print('Error to fetch records')
            return redirect(url_for('index'))
            
        return render_template('read.html', records=records)
        
    except Exception as e:
        print(f'Erro ao carregar registros: {str(e)}')
        return redirect(url_for('index'))
        
    finally:
        if connection and connection.is_connected():
            connection.close()

if __name__ == '__main__':
    app.run(debug=True)