
# SustentaTrack - Sistema de Monitoramento Sustentável


Aplicação web para monitoramento e classificação de indicadores de sustentabilidade, com integração a banco de dados MySQL.

## 🚀 Funcionalidades Principais

- **CRUD Completo**: Crie, leia, atualize e delete registros de consumo
- **Classificação Automática**: Sistema inteligente de categorização de sustentabilidade
- **Dashboard Integrado**: Visualização consolidada dos dados
- **Gestão de Transporte**: Controle de métodos de transporte e seu impacto

## ⚙️ Instalação Local

### Pré-requisitos
- Python 3.8+
- MySQL Server instalado
- Git (opcional)

# Clone o repositório
git clone https://github.com/seu-usuario/sustentatrack.git
cd sustentatrack

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt
```

## 🔧 Configuração

1. **Banco de Dados MySQL**
```sql
CREATE DATABASE pi1;

USE pi1;

CREATE TABLE classificacao_consumo (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sustentabilidade_alta_max DECIMAL(10,2),
    sustentabilidade_baixa_min DECIMAL(10,2)
);

CREATE TABLE classificacao_transportes (
    tipo_transporte VARCHAR(50) PRIMARY KEY,
    classificacao_sustentabilidade VARCHAR(20)
);

CREATE TABLE MONITORAMENTOS_SUSTENTABILIDADE (
    id INT PRIMARY KEY AUTO_INCREMENT,
    data DATE,
    consumo_agua_litros DECIMAL(10,2),
    consumo_energia_kwh DECIMAL(10,2),
    geracao_residuo_porcentagem DECIMAL(5,2),
    transporte_utilizado VARCHAR(50),
    classificacao_sustentabilidade_agua VARCHAR(20),
    classificacao_sustentabilidade_energia VARCHAR(20),
    classificacao_sustentabilidade_residuo VARCHAR(20),
    classificacao_sustentabilidade_transporte VARCHAR(20)
);
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
│   ├── create.html       # Formulário de criação
│   ├── read.html         # Listagem de dados
│   ├── update.html       # Edição de registros
│   └── delete.html       # Exclusão de registros
├── app.py                # Aplicação principal
├── .env                  # Configurações
└── requirements.txt      # Dependências
```

## 🧪 Tecnologias Utilizadas

- **Flask**: Framework web principal
- **MySQL**: Armazenamento de dados
- **Jinja2**: Templates HTML dinâmicos
- **python-dotenv**: Gestão de variáveis de ambiente
- **MySQL Connector**: Interface Python/MySQL

## 📊 Banco de Dados

### Diagrama Entidade-Relacionamento
![Diagrama ER](https://via.placeholder.com/600x400.png?text=Diagrama+ER+do+Banco+de+Dados)

## 🤝 Como Contribuir

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/incrivel`)
3. Commit suas mudanças (`git commit -m 'Adiciona feature incrível'`)
4. Push para a branch (`git push origin feature/incrivel`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

```

Este README fornece uma documentação completa para:
1. Instalação local
2. Configuração do ambiente
3. Estrutura do projeto
4. Operações básicas
5. Gestão do banco de dados
6. Processo de contribuição

Personalize com informações específicas do seu projeto e URLs reais quando disponíveis.