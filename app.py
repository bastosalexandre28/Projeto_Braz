from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# Configuração de conexão com o banco de dados PostgreSQL
db = psycopg2.connect(
    host="localhost",
    port="5432",
    user="postgres",
    password="admin",
    database="plataforma_estudos"
)
cursor = db.cursor()

# Rota principal de cadastro
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        cpf = request.form['cpf']
        rg = request.form['rg']
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        turno = request.form['turno']
        curso = request.form['curso']
        termos_concordados = 'termos' in request.form  # Verifica se o aluno concordou com os termos

        # Verifica se todos os campos obrigatórios foram preenchidos e se os termos foram aceitos
        if not termos_concordados:
            return "Você precisa concordar com os termos para se cadastrar."
        
        # Insere os dados no banco de dados
        cursor.execute("""
            INSERT INTO alunos2 (cpf, rg, nome, email, telefone, turno, curso, termos_concordados)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (cpf, rg, nome, email, telefone, turno, curso, termos_concordados))
        db.commit()
        return redirect(url_for('sucesso', aluno_nome=nome))
    
    return render_template('index.html')

# Rota de sucesso após cadastro
@app.route('/sucesso')
def sucesso():
    aluno_nome = request.args.get('aluno_nome', '')
    return render_template('sucesso.html', aluno_nome=aluno_nome)

if __name__ == '__main__':
    app.run(debug=True)
