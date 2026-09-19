from flask import Flask, render_template, request, send_file, redirect, url_for
import requests
from collections import Counter
import csv
import os
import datetime
import re

app = Flask(__name__)

RESULTS_FILE = 'results.csv'
HISTORY_FILE = 'history.csv'

# Funzione per validare gli URL
url_pattern = re.compile(r'^(https?:\/\/)?([\w.-]+)\.([a-z\.]{2,6})([\/\w .-]*)*\/?$')
def is_valid_url(url):
    return re.match(url_pattern, url) is not None

def save_to_history(entry):
    with open(HISTORY_FILE, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(entry)

def read_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    history = []
    with open(HISTORY_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) == 3:
                history.append({'date': row[0], 'main_server': row[1], 'count': row[2]})
    return history[::-1][-5:]  # Ultimi 5

@app.route('/', methods=['GET', 'POST'])
def index():
    stats = {}
    urls = []
    entries = []
    history = read_history()

    if request.method == 'POST':
        raw_urls = request.form['urls']
        urls = [url.strip() for url in raw_urls.splitlines() if url.strip() and is_valid_url(url.strip())]

        if not urls:
            return render_template('index.html', stats={}, urls=[], history=history)

        server_types = Counter()
        content_types = Counter()
        encodings = Counter()

        for url in urls:
            original_url = url
            if not url.startswith('http'):
                url = 'http://' + url
            try:
                response = requests.head(url, allow_redirects=True, timeout=5)
                headers = response.headers
                server = headers.get('Server', 'Unknown')
                content_type = headers.get('Content-Type', 'Unknown')
                encoding = headers.get('Content-Encoding', 'None')

                server_types[server] += 1
                content_types[content_type] += 1
                encodings[encoding] += 1

                entries.append({
                    'URL': original_url,
                    'Server': server,
                    'Content-Type': content_type,
                    'Content-Encoding': encoding
                })
            except Exception as e:
                print(f"Errore nell'analizzare {url}: {e}")
                server_types['Errore'] += 1
                entries.append({
                    'URL': original_url,
                    'Server': 'Errore',
                    'Content-Type': 'Errore',
                    'Content-Encoding': 'Errore'
                })

        with open(RESULTS_FILE, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['URL', 'Server', 'Content-Type', 'Content-Encoding']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for entry in entries:
                writer.writerow(entry)

        stats = {
            'server': dict(server_types),
            'content': dict(content_types),
            'encoding': dict(encodings),
            'details': entries
        }

        # Aggiungi alla cronologia
        if server_types:
            most_common = server_types.most_common(1)[0][0]
            save_to_history([datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), most_common, str(len(urls))])

        history = read_history()

    return render_template('index.html', stats=stats, urls=urls, history=history)

@app.route('/download')
def download():
    if os.path.exists(RESULTS_FILE):
        return send_file(RESULTS_FILE, as_attachment=True)
    return "Nessun file disponibile", 404

if __name__ == '__main__':
    app.run(debug=True)
