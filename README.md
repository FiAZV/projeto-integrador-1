
# Sistema de Monitoramento Sustentável


Aplicação web para monitoramento e classificação de indicadores de sustentabilidade, com integração a banco de dados MySQL.

## 🚀 Funcionalidades Principais

- **CRUD Completo**: Crie, leia, atualize e delete registros de consumo
- **Classificação Automática**: Sistema inteligente de categorização de sustentabilidade

## ⚙️ Instalação Local

### Pré-requisitos
- Python 3.8+
- MySQL Server instalado
- Git (opcional)

# Clone o repositório
git clone [https://github.com/seu-usuario/sustentatrack.git](https://github.com/FiAZV/projeto-integrador-1.git)
cd sustentatrack

# Instale as dependências
pip install -r requirements.txt

## 🔧 Configuração

1. **Banco de Dados MySQL**
```sql
CREATE DATABASE pi1;

USE pi1;

CREATE TABLE IF NOT EXISTS MONITORAMENTOS_SUSTENTABILIDADE (
    id INT PRIMARY KEY AUTO_INCREMENT UNIQUE,
    data DATE NOT NULL,
    consumo_agua_litros FLOAT,
    consumo_energia_kwh FLOAT,
    geracao_residuo_porcentagem FLOAT,
    transporte_utilizado VARCHAR(255),
    classificacao_sustentabilidade_agua VARCHAR(50),	
    classificacao_sustentabilidade_energia VARCHAR(50),
    classificacao_sustentabilidade_residuo VARCHAR(50),
    classificacao_sustentabilidade_transporte VARCHAR(50)
);

-- Tabela CLASSIFICACAO_CONSUMO
CREATE TABLE IF NOT EXISTS CLASSIFICACAO_CONSUMO (
    id INT PRIMARY KEY AUTO_INCREMENT UNIQUE,
    tipo_consumo VARCHAR(255) NOT NULL,
    unidade_medida VARCHAR(50) NOT NULL,
    sustentabilidade_alta_max FLOAT NOT NULL,
    sustentabilidade_baixa_min FLOAT NOT NULL
);

-- Tabela CLASSIFICACAO_TRANSPORTES
CREATE TABLE IF NOT EXISTS CLASSIFICACAO_TRANSPORTES (
    id INT PRIMARY KEY AUTO_INCREMENT UNIQUE,
    tipo_transporte VARCHAR(50) NOT NULL,
    classificacao_sustentabilidade VARCHAR(50) NOT NULL
);

-- Inserção dos dados de classificação de consumo de água
INSERT INTO CLASSIFICACAO_CONSUMO (tipo_consumo, unidade_medida, sustentabilidade_alta_max, sustentabilidade_baixa_min)
VALUES 
('Consumo de Água', 'litros', 150, 200);

-- Inserção dos dados de classificação de consumo de energia elétrica
INSERT INTO CLASSIFICACAO_CONSUMO (tipo_consumo, unidade_medida, sustentabilidade_alta_max, sustentabilidade_baixa_min)
VALUES 
('Consumo de Energia Elétrica', 'kWh', 5, 10);

-- Inserção dos dados de classificação de geração de resíduos não recicláveis
INSERT INTO CLASSIFICACAO_CONSUMO (tipo_consumo, unidade_medida, sustentabilidade_alta_max, sustentabilidade_baixa_min)
VALUES 
('Geração de Resíduos Não Recicláveis', '%', 20, 50);

-- Inserção dos dados de classificação de transporte
INSERT INTO CLASSIFICACAO_TRANSPORTES (tipo_transporte, classificacao_sustentabilidade)
VALUES 
('bicicleta', 'alta'),
('transporte_publico', 'alta'),
('transporte_eletrico', 'alta'),
('misto_publico_privado', 'moderada'),
('combustivel_fossil', 'baixa');

```

2. **Arquivo .env** (na raiz do projeto)
```ini
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha
DB_DATABASE=pi1
SECRET_KEY=chave_secreta_flask
```

## 🖥️ Execução

```bash
# Inicie o servidor Flask
python app.py
```

Acesse no navegador:  
[http://localhost:5000](http://localhost:5000)

## 🌐 Rotas Principais

| Rota       | Método | Descrição               |
|------------|--------|-------------------------|
| /          | GET    | Página inicial          |
| /create    | GET    | Formulário de criação   |
| /read      | GET    | Listagem de registros   |
| /update    | POST   | Atualização de registro |
| /delete    | POST   | Exclusão de registro    |

## 🛠️ Estrutura do Projeto

```
sustentatrack/
├── backend/
│   └── utils.py          # Lógica de negócio e database
├── static/
│   └── css/
│       └── styles.css    # Estilos principais
├── templates/
│   ├── index.html        # Homepage
│   ├── create.html       # Formulário de criação
│   ├── read.html         # Listagem de dados
│   ├── update.html       # Edição de registros
│   └── delete.html       # Exclusão de registros
├── app.py                # Aplicação principal
├── .env                  # Configurações
└── requirements.txt      # Dependências
```
----
## 📋 Guia de Uso Passo a Passo
- ### 1. Página Inicial (Home)
    Acesse http://localhost:5000.
    
    Navegue usando os botões:

    - 🟢 Inserir Registro: Para cadastrar novos dados.

    - 📋 Listar Registros: Para visualizar todos os registros.
    
    - ✏️ Alterar Registro: Para editar dados existentes.
    
    - 🗑️ Excluir Registro: Para remover registros permanentemente

- ### 2. Inserir Registro
    Clique em "Inserir Registro" na Home.
    
    Preencha o formulário:
    
    - Data: Formato AAAA-MM-DD (ex: 2023-10-20).
    
    - Água (L): Valores decimais com ponto (ex: 150.5).
    
    - Energia (kWh): Exemplo: 8.3.
    
    - Resíduos (%): Entre 0 e 100 (ex: 75).
    
    - Transporte: Selecione uma opção do menu.
    
    Clique em 🔄 Salvar Registro.

- ### 3. Listar Registros
    Clique em "Listar Registros" na Home.
    
    A tabela mostrará: ID, data, consumo de água/energia, resíduos, transporte.
    
    Classificações: Cores ou rótulos automáticos (ex: alta, moderada).
    
- ### 4. Alterar Registro
    Clique em "Alterar Registro" na Home.
    
    Insira o ID do Registro (ex: 5).
    
    Edite os campos desejados.
    
    Clique em ✏️ Atualizar Registro.

- ### 5. Excluir Registro
    Clique em "Excluir Registro" na Home.
    
    Insira o ID do Registro (ex: 3).
    
    Confirme com 🗑️ Confirmar Exclusão.

- ### 6. Dicas Importantes
    Validações:
    
    Insira apenas valores positivos
    
    Decimais usam ponto (ex: 10.5).
    
    Transporte: Use exatamente as opções do menu.
    
    Erros Comuns:
    
    Campos vazios ou formatos inválidos bloqueiam o envio.
    
    IDs inexistentes exibem mensagens de erro.
