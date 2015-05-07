import pystache, csv, json, sqlite3, sys

if len(sys.argv) != 2:
    print('usage: %s SUGGESTIONS')
    exit()

suggestions_filename = sys.argv[1]

with open('tags.csv') as f:
    reader = csv.reader(f)
    tags = [row[1] for row in reader]

with open(suggestions_filename) as f:
    data = json.loads(f.read())

conn = sqlite3.connect('docs.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

rows = []
for id in data['suggestions']:
    cur.execute('select id, title, url, description from docs where id = ?', (id, ))
    row = cur.fetchone()
    rows.append(dict(row))

conn.close()

with open('templates/suggestions.html') as f:
    print(pystache.render(f.read(), {'tags': tags, 'raw_tags': json.dumps(tags), 'documents': rows}))
