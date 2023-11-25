


from flask import Flask, render_template, request, redirect, url_for

import pymysql

db = pymysql.connect(host="127.0.0.1",
                     user="root",
                     password="2127190126",
                     database="validar_cpf")

app = Flask(__name__)

def calcula_cpf(cpf):
  # Remove caracteres não numéricos
  cpf = ''.join(filter(str.isdigit, cpf))

  # Verifica se o CPF tem 11 dígitos ou se todos são iguais
  if len(cpf) != 11 or len(set(cpf)) == 1:
      return False

  v1 = v2 = 0
  for i in range(9):
      v1 += int(cpf[8 - i]) * (9 - (i % 10))
      v2 += int(cpf[8 - i]) * (9 - ((i + 1) % 10))

  v1 = (v1 % 11) % 10
  v2 += v1 * 9
  v2 = (v2 % 11) % 10

  
  return cpf.endswith(str(v1) + str(v2))

@app.route('/') #abre a pasta template e o arquivo 'html' 
def index():
    cursor = db.cursor()
    sql = "SELECT * FROM parceiros;"
    cursor.execute(sql)
    parceiros = cursor.fetchall()
    return render_template('index.html', parceiros=parceiros)


@app.route('/validar_cpf', methods=['POST'])
def validar_cpf():
    cpf=request.form['cpf']


    if calcula_cpf(cpf):

        nome = request.form['nome']
        cursor = db.cursor()
        #
        sql = "INSERT INTO parceiros (cpf, nome) VALUES ('"
        sql += cpf + "','" + nome + "');"
        #
        cursor.execute(sql)
        #
        db.commit()

        return '<p>CPF válido e processado.</p>' +\
                '<p> Para inserir um novo parceiro, clique <a href="http://127.0.0.1:5000/">aqui</p>'
    else:
        return '<p style="color:red">CPF <b>inválido</b>.</p>' +\
                '<button onclick="history.back()">Voltar</button>'
    
@app.route('/atualizar_parceiro', methods=['POST'])
def atualizar_parceiro():
    cpf = request.form['cpf']
    nome = request.form['nome']
    cursor = db.cursor()
    sql = "UPDATE parceiros SET nome = %s WHERE cpf = %s"
    cursor.execute(sql, (nome,cpf))
    db.commit()
    return redirect(url_for('index'))

@app.route('/excluir_parceiro', methods =  ['POST'])
def excluir_parceiro():
    cpf = request.form['cpf']
    cursor = db.cursor()
    sql = "DELETE FROM parceiros WHERE cpf = %s"
    cursor.execute(sql, (cpf))
    db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)




    

