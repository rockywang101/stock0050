CREATE TABLE STOCK_DAILY (
	ID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
	STOCK_ID TEXT,
	TX_DATE TEXT,
	TX_AMOUNT INTEGER,
	TX_MONEY INTEGER,
	OPEN_PRICE REAL,
	HIGHEST_PRICE REAL,
	LOWEST_PRICE REAL,
	CLOSE_PRICE REAL,
	CREATE_TIME DATE
)
