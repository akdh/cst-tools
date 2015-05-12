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
for index in range(len(data['suggestions'])):
    id = data['suggestions'][index]
    cur.execute('select id, title, url, description from docs where id = ?', (id, ))
    row = dict(cur.fetchone())
    row['index'] = index
    rows.append(rows)

conn.close()

with open('templates/suggestions.html') as f:
    print(pystache.render(f.read(), {'tags': tags, 'raw_tags': json.dumps(tags), 'documents': rows}))
