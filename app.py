from flask import Flask, render_template, request
from flask_ngrok import run_with_ngrok
import requests
import json
import pandas as pd


def get_ngrok_url():
    url = "http://localhost:4040/api/tunnels/"
    res = requests.get(url)
    res_unicode = res.content.decode("utf-8")
    res_json = json.loads(res_unicode)
    for i in res_json["tunnels"]:
        if i['name'] == 'command_line':
            return i['public_url']
            break
            
app = Flask('app_news')
run_with_ngrok(app)  # Start ngrok when app is run

@app.route('/')
def show_start_form():
    link=get_ngrok_url()+'/result'
    return render_template('form.html', link=link)
@app.route('/result', methods=['POST'])


def result():
    
	form = request.form
	if request.method == 'POST':
		rss = request.form['rss']
		df=pd.read_csv('/content/app_news/articles.csv', delimiter=',')		
		df=df[['category','result','title','lang', 'link', 'tone']].sort_values('result',ascending=False)
		#df.style.format({'link': make_clickable})
		df1=df[df.category=="technology"]
		df2=df[df.category=="science"]
		df3=df[df.category=="society"]
		df4=df[df.category=="not_news"]
		df5=df[df.category=="real_estate"]
    
       #predict = model.predict(n) #получение результата прогнозирования
	return render_template('resultsform.html', tables1=[df1.to_html(classes='data')], titles1=df1.columns.values, tables2=[df2.to_html(classes='data')], titles2=df2.columns.values, tables3=[df3.to_html(classes='data')], titles3=df3.columns.values, tables4=[df4.to_html(classes='data')], titles4=df4.columns.values, tables5=[df5.to_html(classes='data')], titles5=df5.columns.values, rss=rss,)

@app.route('/main.html')
def main():
    return render_template('main.html')
    
app.run()