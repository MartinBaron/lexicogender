CREATE TABLE lexico_element(
   id_lexico_element INTEGER PRIMARY KEY AUTOINCREMENT,
   title           TEXT    NOT NULL,
   url        TEXT NOT NULL,
   lexico TEXT NOT NULL,
   lexico_url TEXT NOT NULL,
   feminin            BOOLEAN NOT NULL DEFAULT false,
   masculin            BOOLEAN NOT NULL DEFAULT false
);