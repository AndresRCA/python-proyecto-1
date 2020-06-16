from os import path
from classes.db_model.enums.Toppings import Toppings
from classes.db_model.enums.Sizes import Sizes
import sqlite3

class SQLiteDB:
	"""SQLiteDB es una clase Singleton que maneja la base de datos y sus operaciones"""
	
	__instance = None # connection instance
	
	# fixed values stored in database (needed for creating the database), should get extracted and not initialized when db is already up
	__size_ids = (Sizes.PERSONAL, Sizes.MEDIUM, Sizes.FAMILY)
	__size_names = ('personal', 'mediano', 'familiar')
	__size_prices = (10, 15, 20)
	__topping_names = [('jamón',), ('champiñones',), ('pimentón',), ('doble queso',), ('aceitunas',), ('pepperoni',), ('salchichón',)]
	__topping_prices = {
		Toppings.HAM.value: (1.5, 1.75, 2.00), 
		Toppings.MUSHROOM.value: (1.75, 2.05, 2.50), 
		Toppings.BELL_PEPPER.value: (1.5, 1.75, 2.00), 
		Toppings.DOUBLE_CHEESE.value: (0.80, 1.30, 1.70), 
		Toppings.OLIVE.value: (0.80, 2.15, 2.60), 
		Toppings.PEPPERONI.value: (1.25, 1.70, 1.90), 
		Toppings.SAUSAGE.value: (1.60, 1.85, 2.10)
	}
	
	@staticmethod 
	def getInstance():
		"""Metodo estatico de acceso"""
		if SQLiteDB.__instance == None:
			SQLiteDB()
		return SQLiteDB.__instance
	
	def __init__(self):
		SQLiteDB.__instance = self.setUp()
			
	def setUp(self):
		"""Crea DB e inicialización. Retorna la conexión"""
		if path.exists('./DB/Store.db'):
			db = sqlite3.connect('./DB/Store.db')
			print('database exists')
			return db
		
		print("database doesn't exist")
		db = sqlite3.connect('./DB/Store.db')
		cursor = db.cursor()
		
		#cursor.execute('SET CHARACTER utf8')
		# create every table in the DB
		self.initSizesTable(cursor)
		self.initToppingsTable(cursor)
		self.initOrdersTable(cursor)
		self.initPizzasTable(cursor)
		self.initPizzaTopping(cursor)
		self.initToppingPricesTable(cursor)
		
		db.commit()
		return db
		
	def initSizesTable(self, cursor):
		"""Crea la tabla Sizes si Store.db no existe"""
		cursor.execute('CREATE TABLE IF NOT EXISTS Sizes (SizeId INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR NOT NULL, price INT)')
		cursor.executemany('INSERT INTO Sizes (name, price) VALUES (?,?)', zip(self.__size_names, self.__size_prices))
		
	def initToppingsTable(self, cursor):
		"""Crea la tabla Toppings si Store.db no existe"""
		cursor.execute('CREATE TABLE IF NOT EXISTS Toppings (ToppingId INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR NOT NULL)')
		cursor.executemany('INSERT INTO Toppings (name) VALUES (?)', self.__topping_names)
		
	def initOrdersTable(self, cursor):
		"""Crea la tabla Orders si Store.db no existe"""
		cursor.execute('CREATE TABLE IF NOT EXISTS Orders (OrderId INTEGER PRIMARY KEY AUTOINCREMENT, client_name VARCHAR NOT NULL, order_date DATE NOT NULL, total FLOAT NOT NULL)')
		
	def initPizzasTable(self, cursor):
		"""Crea la tabla Pizzas si Store.db no existe"""
		cursor.execute('''CREATE TABLE IF NOT EXISTS Pizzas (PizzaId INTEGER PRIMARY KEY AUTOINCREMENT, total FLOAT NOT NULL, 
						SizeId INTEGER, OrderId INTEGER, 
						FOREIGN KEY (SizeId) REFERENCES Sizes(SizeId), 
						FOREIGN KEY (OrderId) REFERENCES Orders(OrderId))''')
	
	def initPizzaTopping(self, cursor):
		"""Crea la tabla PizzaTopping si Store.db no existe"""
		cursor.execute('''CREATE TABLE IF NOT EXISTS PizzaTopping (PizzaId INTEGER, ToppingId Integer, 
					   FOREIGN KEY (PizzaId) REFERENCES Pizzas(PizzaId), 
					   FOREIGN KEY (ToppingId) REFERENCES Toppings(ToppingId))''')
		
	def initToppingPricesTable(self, cursor):
		"""Crea la tabla ToppingPrices si Store.db no existe"""
		cursor.execute('''CREATE TABLE IF NOT EXISTS ToppingPrices (price FLOAT NOT NULL, SizeId INTEGER, ToppingId INTEGER, 
						FOREIGN KEY (SizeId) REFERENCES Pizzas(PizzaId)
						FOREIGN KEY (ToppingId) REFERENCES Toppings(ToppingId))''')
		values = self.getToppingPricesRows()
		cursor.executemany('INSERT INTO ToppingPrices (price, SizeId, ToppingId) VALUES (?,?,?)', values) # insert multiple rows here (for each ToppingId)
	
	def getToppingPricesRows(self):
		"""Retorna una lista de tuplas [(price, SizeId, ToppingId)] para el uso de cursor.executemany() en ToppingPricesTable()"""
		return [(price, size_id.value, topping.value) for topping in Toppings for size_id, price in zip(self.__size_ids, self.__topping_prices[topping.value])]
	
	@property
	def instance(self):
		return self.__instance