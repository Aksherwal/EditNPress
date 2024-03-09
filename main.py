from flask import Flask, render_template, request, redirect, url_for, jsonify
import psycopg2
import requests
from clean_it import clean_it

app = Flask(__name__)

# Connect to PostgreSQL
conn=psycopg2.connect(
host="localhost", database="dhp2024", user="postgres", password="aks@sitare")
cur=conn.cursor()

# Create the table if it doesn't exist (adjust columns as needed)
cur.execute("""CREATE TABLE IF NOT EXISTS News_Content (id serial primary key,
        URL varchar,
        Given_text text,
        Words_count int,
        Sentence_count int,
        Stop_words_count int,
        UPOS_tags_info text,
        Most_frequent_words text
        )
""")
conn.commit()

# Route for home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling form submission
@app.route('/submit', methods=['POST', 'GET'])
def submit():
    if request.method == 'POST':
        url = request.form['url']
    # checking validity of given URL
    if url.startswith("https://indianexpress.com/article/") and requests.head(url).status_code==200:
        
        url,clean_text_result,words_count,sent_count,count_stop_words,upos_text,most_freq_words=clean_it(url)
        cur.execute("""INSERT INTO News_Content(
        URL,
        Given_text,
        Words_count,
        Sentence_count,
        Stop_words_count,
        UPOS_tags_info,
        Most_frequent_words) VALUES (%s,%s,%s,%s,%s,%s,%s) on conflict do nothing""",(url,clean_text_result,words_count,sent_count,count_stop_words,upos_text,most_freq_words))
        conn.commit()
        return redirect(url_for('result'))
    
    else:
        text='Please enter a valid URL from IndianExpress website!'
        return render_template('index.html',text=text)

# Route for displaying processed text
@app.route('/result')
def result():
    # cur.execute("DELETE from News_Content where Given_text=''")
    # conn.commit()
    cur.execute("SELECT * FROM News_Content ORDER BY id DESC LIMIT 1")
    article = cur.fetchall() 
    cur.execute("SELECT URL FROM News_Content ORDER BY id DESC LIMIT 1")
    url=cur.fetchall()
    return render_template('result.html', article=article,url=url)

@app.route('/plain_text')
def plain_text():
    # cur.execute("DELETE from News_Content where Given_text=''")
    # conn.commit()
    cur.execute("SELECT Given_text FROM News_Content ORDER BY id DESC LIMIT 1")
    cleantext = cur.fetchall() 
    return render_template('plain_text.html', news_text=cleantext)
@app.route('/login', methods=['POST','GET'])
def login():
    user=''
    paswd=''
    mesg=''
    if request.method=='POST':
        user=request.form['Username']
        paswd=request.form['Password']
    if user=='admin@example.com' and paswd=='12345':
        return render_template('admin.html')
    else:
        mesg='Wrong ID or Password'
        return render_template('login.html',mesg=mesg)
@app.route('/login_page')
def login_page():
    return render_template('login.html')
    
@app.route('/view_history')
def view_history():
    cur.execute("SELECT * FROM News_Content")
    full_history = cur.fetchall() 
    return render_template('history.html', history=full_history)
@app.route('/clear_history')
def clear_history():
    mesg='History is cleared!'
    cur.execute("Delete from News_Content")
    conn.commit()
    cur.execute('ALTER SEQUENCE News_Content_id_seq RESTART WITH 1')
    conn.commit()
    return render_template('history.html',mesg=mesg)

if __name__ == '__main__':
    app.run(debug=True)


