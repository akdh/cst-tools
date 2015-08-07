.mode csv
CREATE TABLE docs (id TEXT PRIMARY KEY, location INT, url TEXT, title TEXT);
.import collection_2015.csv docs
