CREATE TABLE IF NOT EXISTS CURRENCY(ID INTEGER PRIMARY KEY, NAME TEXT, BALANCE INTEGER);
CREATE TABLE IF NOT EXISTS CRYPTO(ID INTEGER, NAME TEXT, AMOUNT REAL, COIN TEXT,PRIMARY KEY (ID, COIN));