# 📌 Personal Finance Manager

## **1️⃣ Visão Geral do Projeto**
O **Personal Finance Manager** é um sistema desenvolvido em **Django** que permite aos usuários gerenciar suas finanças pessoais de forma eficiente. O sistema oferece funcionalidades como **cadastro de transações financeiras (receitas e despesas), categorização dos gastos, definição de metas financeiras e geração de relatórios detalhados**.

O objetivo do sistema é permitir que os usuários acompanhem suas finanças de forma organizada, facilitando a tomada de decisões baseadas em dados financeiros.

---

## **2️⃣ Objetivos do Sistema**
O sistema foi projetado para atender as seguintes necessidades:
✅ **Registrar transações financeiras** (entradas e saídas de dinheiro).  
✅ **Classificar transações por categoria** para melhor organização financeira.  
✅ **Definir metas financeiras** para planejamento pessoal.  
✅ **Gerar relatórios financeiros** em diferentes formatos (PDF, Excel).  
✅ **Fornecer uma API RESTful** para integração com outras plataformas.  
✅ **Garantir a segurança dos dados dos usuários**, permitindo apenas acesso autorizado às informações.

---

## **3️⃣ Funcionalidades do Sistema**
O sistema será dividido nos seguintes módulos:

### 🔹 **1. Autenticação e Gerenciamento de Usuários**
- Cadastro e login de usuários.
- Recuperação de senha via e-mail.
- Permitir que cada usuário visualize apenas seus próprios dados.

### 🔹 **2. Categorias**
- Criar categorias para classificar transações financeiras.
- As categorias podem ser **Receita (Income), Despesa (Expense)** ou **Mista (Mixed)**.
- Cada usuário pode ter suas próprias categorias personalizadas.

### 🔹 **3. Transações**
- Cadastrar receitas e despesas financeiras.
- Associar cada transação a uma categoria.
- Permitir edição e exclusão de transações.
- Listar todas as transações filtrando por **data, categoria e tipo (receita ou despesa)**.

### 🔹 **4. Metas Financeiras**
- Criar metas de economia ou limite de gastos.
- Definir metas mensais ou anuais.
- Associar metas a uma categoria específica ou globalmente.

### 🔹 **5. Relatórios e Análises**
- Exibir estatísticas financeiras com gráficos.
- Gerar relatórios de **receitas e despesas por período**.
- Exportar relatórios em **PDF ou Excel**.
- Enviar relatórios agendados por e-mail.

### 🔹 **6. API RESTful**
- Criar uma API estruturada para interagir com o sistema via **JSON**.
- Implementar autenticação com **JWT** para proteger os endpoints.
- Permitir integração com **outros aplicativos e plataformas**.

---

## **4️⃣ Estrutura das Entidades e Relacionamentos**
O sistema possui quatro entidades principais: **Usuário, Categoria, Transação e Meta Financeira**.

### 🧑 **1. Usuário (`User`)**
Armazena os dados de autenticação dos usuários.

| Campo       | Tipo de Dado       | Descrição |
|------------|-------------------|-----------|
| `id`       | Integer (PK)       | Identificador único do usuário. |
| `email`    | Email (Único)      | E-mail usado para login. |
| `first_name` | String (Máx 30) | Primeiro nome do usuário. |
| `last_name`  | String (Máx 30) | Sobrenome do usuário. |
| `password`  | String (Hashed)   | Senha criptografada do usuário. |
| `is_active` | Boolean          | Indica se o usuário está ativo. |
| `is_staff`  | Boolean          | Indica se o usuário é administrador. |

### 📂 **2. Categoria (`Category`)**
Representa os diferentes tipos de receitas e despesas que um usuário pode ter.

| Campo      | Tipo de Dado     | Descrição |
|-----------|-----------------|-----------|
| `id`      | Integer (PK)     | Identificador único da categoria. |
| `user`    | FK → `User`      | Categoria pertence a um usuário. |
| `name`    | String (Máx 100) | Nome da categoria. |
| `type`    | Enum (income, expense, mixed) | Tipo da categoria. |

### 💰 **3. Transação (`Transaction`)**
Representa uma movimentação financeira de entrada ou saída.

| Campo       | Tipo de Dado     | Descrição |
|------------|-----------------|-----------|
| `id`       | Integer (PK)     | Identificador único da transação. |
| `user`     | FK → `User`      | Usuário dono da transação. |
| `category` | FK → `Category`  | Categoria da transação. |
| `type`     | Enum (income, expense) | Tipo da transação. |
| `date`     | Date            | Data da transação. |
| `amount`   | Decimal(10,2)   | Valor da transação. |
| `description` | Text (Opcional) | Descrição da transação. |

### 🎯 **4. Meta Financeira (`Goal`)**
Define objetivos financeiros do usuário.

| Campo        | Tipo de Dado     | Descrição |
|-------------|-----------------|-----------|
| `id`        | Integer (PK)     | Identificador único da meta. |
| `user`      | FK → `User`      | Meta pertence a um usuário. |
| `category`  | FK → `Category` (Opcional) | Meta pode ser vinculada a uma categoria. |
| `name`      | String (Máx 200) | Nome da meta. |
| `target_amount` | Decimal(10,2) | Valor desejado para atingir. |
| `frequency` | Enum (monthly, yearly) | Frequência da meta. |

---

## **5️⃣ API Endpoints e URLs**
A API seguirá uma estrutura **RESTful**, garantindo organização e boas práticas.

### **1️⃣ Usuários (`/api/users/`)**
| Método | Rota               | Descrição |
|--------|--------------------|-----------|
| `POST` | `/register/`       | Criar um novo usuário. |
| `POST` | `/login/`          | Autenticar um usuário. |
| `GET`  | `/profile/`        | Retorna os dados do usuário logado. |

### **2️⃣ Categorias (`/api/categories/`)**
| Método | Rota               | Descrição |
|--------|--------------------|-----------|
| `POST` | `/categories/`     | Criar uma categoria. |
| `GET`  | `/categories/`     | Listar todas as categorias do usuário. |

### **3️⃣ Transações (`/api/transactions/`)**
| Método | Rota               | Descrição |
|--------|--------------------|-----------|
| `POST` | `/transactions/`   | Criar uma transação. |
| `GET`  | `/transactions/`   | Listar todas as transações do usuário. |

---
