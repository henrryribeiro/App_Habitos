import sqlite3

# Função para conectar ao banco de dados
def conectar_bd():
    return sqlite3.connect('habit_tracker.db')

# Função para criar as tabelas
def criar_tabelas():
    conn = conectar_bd()
    cursor = conn.cursor()
    
    # Criar a tabela de usuários
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    )
    ''')
    
    # Criar a tabela de hábitos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS habits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        habit_name TEXT NOT NULL,
        start_date DATE NOT NULL,
        goal TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    # Criar a tabela de registros diários
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER NOT NULL,
        log_date DATE NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (habit_id) REFERENCES habits (id)
    )
    ''')
    
    conn.commit()
    conn.close()

# Função para inserir um usuário
def inserir_usuario(nome, email):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (name, email)
            VALUES (?, ?)
        ''', (nome, email))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Erro: O e-mail {email} já está cadastrado.")
    finally:
        conn.close()

# Função para inserir um hábito
def inserir_habito(user_id, habit_name, start_date, goal=None):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO habits (user_id, habit_name, start_date, goal)
        VALUES (?, ?, ?, ?)
    ''', (user_id, habit_name, start_date, goal))
    conn.commit()
    conn.close()

# Função para inserir um registro diário
def inserir_registro_diario(habit_id, log_date, status):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO daily_logs (habit_id, log_date, status)
        VALUES (?, ?, ?)
    ''', (habit_id, log_date, status))
    conn.commit()
    conn.close()

# Função para listar todos os usuários
def listar_usuarios():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

# Função para listar todos os hábitos
def listar_habitos():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM habits')
    habitos = cursor.fetchall()
    conn.close()
    return habitos

# Função para listar todos os registros diários
def listar_registros_diarios():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM daily_logs')
    registros = cursor.fetchall()
    conn.close()
    return registros

# Criar as tabelas
criar_tabelas()

# Inserir usuários
inserir_usuario('João Silva', 'joao@email.com')
inserir_usuario('Maria Oliveira', 'maria@email.com')
inserir_usuario('Pedro Santos', 'pedro@email.com')
inserir_usuario('Ana Souza', 'ana@email.com')

# Inserir hábitos
inserir_habito(1, 'Correr', '2024-08-01', 'Correr 5 km por dia')
inserir_habito(2, 'Ler', '2024-08-01', 'Ler 20 páginas por dia')
inserir_habito(3, 'Meditar', '2024-08-01', 'Meditar por 10 minutos')
inserir_habito(4, 'Beber Água', '2024-08-01', 'Beber 2 litros de água')

# Inserir registros diários
inserir_registro_diario(1, '2024-08-01', 'Completo')
inserir_registro_diario(1, '2024-08-02', 'Não Completo')
inserir_registro_diario(2, '2024-08-01', 'Completo')
inserir_registro_diario(2, '2024-08-02', 'Completo')
inserir_registro_diario(3, '2024-08-01', 'Completo')
inserir_registro_diario(3, '2024-08-02', 'Não Completo')
inserir_registro_diario(4, '2024-08-01', 'Completo')
inserir_registro_diario(4, '2024-08-02', 'Completo')

# Exibir os dados inseridos
print("Usuários:")
for usuario in listar_usuarios():
    print(usuario)

print("\nHábitos:")
for habito in listar_habitos():
    print(habito)

print("\nRegistros Diários:")
for registro in listar_registros_diarios():
    print(registro)

import tkinter as tk
from tkinter import messagebox

# Função para adicionar um novo hábito
def adicionar_habito():
    nome_habito = entry_habito.get()
    data_inicio = entry_data_inicio.get()
    if nome_habito and data_inicio:
        # Aqui você adicionaria o hábito ao banco de dados
        messagebox.showinfo("Sucesso", "Hábito adicionado com sucesso!")
    else:
        messagebox.showwarning("Erro", "Por favor, preencha todos os campos.")

# Configuração da janela principal
root = tk.Tk()
root.title("Controle de Hábitos")

# Campo para o nome do hábito
tk.Label(root, text="Nome do Hábito:").grid(row=0, column=0)
entry_habito = tk.Entry(root)
entry_habito.grid(row=0, column=1)

# Campo para a data de início
tk.Label(root, text="Data de Início (AAAA-MM-DD):").grid(row=1, column=0)
entry_data_inicio = tk.Entry(root)
entry_data_inicio.grid(row=1, column=1)

# Botão para adicionar o hábito
tk.Button(root, text="Adicionar Hábito", command=adicionar_habito).grid(row=2, column=0, columnspan=2)

# Iniciar a interface
root.mainloop()

import matplotlib.pyplot as plt

# Exemplo de dados de progresso
datas = ['2024-08-01', '2024-08-02', '2024-08-03', '2024-08-04']
status = [1, 0, 1, 1]  # 1 para completo, 0 para não completo

# Criar um gráfico de linha para mostrar o progresso
plt.plot(datas, status, marker='o')
plt.title('Progresso do Hábito')
plt.xlabel('Data')
plt.ylabel('Status (1 = Completo, 0 = Não Completo)')
plt.grid(True)
plt.show()

import schedule
import time

def enviar_lembrete():
    print("Lembrete: Não se esqueça de completar seu hábito de hoje!")

# Agendar o lembrete para ser enviado todos os dias às 9h
schedule.every().day.at("09:00").do(enviar_lembrete)

# Função para gerar o relatório semanal
def gerar_relatorio_semanal():
    # Suponha que extraímos dados do banco de dados
    progresso_semanal = {
        '2024-08-01': 1,
        '2024-08-02': 0,
        '2024-08-03': 1,
        '2024-08-04': 1,
        '2024-08-05': 1,
        '2024-08-06': 0,
        '2024-08-07': 1,
    }
    completados = sum(progresso_semanal.values())
    total_dias = len(progresso_semanal)
    relatorio = f"Você completou {completados} de {total_dias} dias nesta semana."
    print(relatorio)

# Loop para executar os lembretes
while True:
    schedule.run_pending()
    time.sleep(1)