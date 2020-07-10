# -*- coding: utf-8 -*-
from flask import Flask,render_template, request, Markup, flash
from conectarBD import Conect
import glob
import json
import datetime

app = Flask(__name__)
bd = Conect()

@app.route('/')
def home():
	select = ''
	ano = bd.select('EXTRACT(YEAR FROM data)','tb_currents','TRUE group by EXTRACT(YEAR from data) order by EXTRACT(YEAR from data)')
	mes = datetime.datetime.now().month
	thDia = datetime.datetime.now().day
	for item in ano:
		select += '<option value="'+str(item[0])+'">'+str(int(item[0]))+'</option>'
	optsAno = Markup(select)
	select = ''
	lstM = ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']
	meses = bd.select('EXTRACT(MONTH FROM data)','tb_currents','TRUE group by EXTRACT(YEAR FROM data), EXTRACT(MONTH FROM data) order by EXTRACT(YEAR FROM data), EXTRACT(MONTH FROM data) desc')
	for item in meses:
		select += '<option value="'+str(item[0])+'">'+lstM[int(item[0]-1)]+'</option>'
	optsMes = Markup(select)

	return render_template('plot.html', optsAno = optsAno, optsMes=optsMes, thMes=lstM[int(meses[0][0]-1)], thDia=thDia)

@app.route('/tbData', methods=['POST'])
def tbFncs():
	rp = {}
	condicao = ''
	now = datetime.datetime.now()
	if 'mes' in request.form:
		condicao = 'EXTRACT(DAY FROM data)<='+str(now.day)+' and EXTRACT(MONTH FROM data)='+str(request.form['mes'])+' and EXTRACT(YEAR FROM data)='+str(request.form['ano'])
	result = bd.select('distinct on (a.id) a.id, a.local','tb_arduinos as a left join tb_currents as c on (a.id=c.id_arduino and '+condicao+')','a.status=TRUE order by a.id, c.id desc')
	total = bd.select('sum(totalC)','(select cast(round(avg(c.current),2) as float) as totalC from tb_arduinos as a left join tb_currents as c on a.id=c.id_arduino where a.status=TRUE and '+condicao+' group by EXTRACT(YEAR FROM data), EXTRACT(MONTH FROM data), EXTRACT(DAY FROM data), EXTRACT(HOUR FROM data)) as medias')
	for i, item in enumerate(result):
		item = list(result[i])
		pctLocal = bd.select('sum(md) as totalLocal','(select cast(round(avg(current),2) as float) as md from tb_currents where id_arduino='+str(item[0])+' and '+condicao+' group by EXTRACT(YEAR FROM data), EXTRACT(MONTH FROM data), EXTRACT(DAY FROM data), EXTRACT(HOUR FROM data)) as medias')
		pctLocalHj = bd.select('sum(md) as totalHJ','(select cast(round(avg(current),2) as float) as md from tb_currents where id_arduino='+str(item[0])+' and EXTRACT(DAY FROM data)<='+str(now.day)+' and EXTRACT(MONTH FROM data)='+str(now.month)+' and EXTRACT(YEAR FROM data)='+str(now.year)+' group by EXTRACT(YEAR FROM data), EXTRACT(MONTH FROM data), EXTRACT(DAY FROM data), EXTRACT(HOUR FROM data)) as medias')
		item.append(pctLocalHj[0][0])
		item.append(pctLocal[0][0])
		result[i] = item

	rp = {'tabela':result, 'total':total[0][0]}
	return json.dumps(rp)

@app.route('/graph',methods=['POST'])
def graphFncs():
	condicao = 'TRUE'
	de = request.form['de']
	ate = request.form['ate']
	frequencia = request.form['freq']
	tensao = request.form['tensao']
	dtformt = "'DD/MM/YYYY'"
	if frequencia=='2':
		dtformt = "'DD/MM/YYYY HH24:00'"
	rp = {}
	if de!='':
		condicao = "data >= timestamp '"+str(datetime.datetime.strptime(de, "%d/%m/%Y"))+"'"
	if ate!='':
		if condicao!='':
			condicao+=' and '
		condicao += "data <= timestamp '"+str(datetime.datetime.strptime(ate, "%d/%m/%Y"))+"'"
	rp['labels'] = bd.select("to_char(data, "+dtformt+")","tb_currents",condicao+" group by to_char(data, "+dtformt+") order by min(data)")
	rpLocais = bd.select("a.id, a.local","tb_currents as c left join tb_arduinos as a on c.id_arduino=a.id",condicao+" and a.status=TRUE group by a.id, a.local, to_char(data, "+dtformt+") order by min(data)")
	rp['locais'] = {}
	for i, item in enumerate(rpLocais):
		rp['locais'][item[1]] = bd.select("sum(medias), to_char(data, "+dtformt+") as dt","(select ((cast(avg(c.current) as float)*"+tensao+")/1000) as medias,max(data) as data from tb_currents as c left join tb_arduinos as a on c.id_arduino=a.id where "+condicao+" and a.status=TRUE and c.id_arduino="+str(item[0])+" group by a.local, EXTRACT(YEAR FROM data), EXTRACT(MONTH FROM data), EXTRACT(DAY FROM data), EXTRACT(HOUR FROM data) order by min(data)) as media", "TRUE group by to_char(data, "+dtformt+") order by to_char(data, "+dtformt+")")
	return json.dumps({'rp':rp})

@app.route('/cad',methods=['POST'])
def cadFncs():
	acao = request.form['acao']
	if acao=='lista':
		rp = bd.select('id, ip, local, status','tb_arduinos', 'TRUE order by status desc,id asc')
		return json.dumps({'rp':rp})
	if acao=='salvar':
		local = request.form['local']
		id = request.form['id']
		rp = bd.update('tb_arduinos',"local='"+local+"'",'id='+id)
		return json.dumps({'rp':rp})
	if acao=='io':
		id = request.form['id']
		status = request.form['status']
		if status=='Ativo':
			status = 'FALSE'
		else:
			status = 'TRUE'
		rp = bd.update('tb_arduinos',"status="+status,'id='+id)
		return json.dumps({'rp':rp})

if __name__=="__main__":
	app.run(debug=True)
