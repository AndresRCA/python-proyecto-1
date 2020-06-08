from os import path
from classes.db_model.enums.Toppings import Toppings
import sqlite3

class SQLiteDB:
	"""SQLiteDB es una clase Singleton que maneja la base de datos y sus operaciones"""
	
	__instance = None # connection instance
	
	# fixed values stored in database (needed for creating the database), should get extracted and not initialized when db is already up
	__size_names = ('personal', 'mediano', 'familiar')
	__size_prices = (10, 15, 20)
	__topping_names = ('jamón', 'champiñones', 'pimentón', 'doble queso', 'aceitunas', 'pepperoni', 'salchichón')
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
		
		print('base de datos no existe')
		db = sqlite3.connect('./DB/Store.db')
		cursor = db.cursor()
		
		#cursor.execute('SET CHARACTER utf8')
		# create every table in the DB
		self.createSizesTable(cursor)
		self.createToppingsTable(cursor)
		#self.createPizzasTable(cursor) # in progress
		#self.createToppingPricesTable(cursor) # in progress
		db.commit()
		return db
		
	def createSizesTable(self, cursor):
		"""Crea la tabla Sizes si Store.db no existe"""
		cursor.execute('CREATE TABLE IF NOT EXISTS Sizes (SizeId INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR NOT NULL, price INT)')
		cursor.execute("INSERT INTO Sizes (name, price) VALUES " + ','.join("('{}', {})".format(size, price) for size, price in zip(self.__size_names, self.__size_prices))) # maybe use executemany
		
	def createToppingsTable(self, cursor):
		"""Crea la tabla Toppings si Store.db no existe"""
		cursor.execute('CREATE TABLE IF NOT EXISTS Toppings (ToppingId INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR NOT NULL)')
		cursor.execute("INSERT INTO Toppings (name) VALUES " + ','.join("('{}')".format(topping) for topping in self.__topping_names))
		
	# in progress
	def createPizzasTable(self, cursor):
		"""Crea la tabla Pizzas si Store.db no existe"""
		cursor.execute('''CREATE TABLE IF NOT EXISTS Sales 
						(PizzaId INTEGER PRIMARY KEY AUTOINCREMENT, client_name VARCHAR NOT NULL, sale_date DATE NOT NULL, SizeId INTEGER, CONSTRAINT fk_SizeId FOREIGN KEY (SizeId) REFERENCES Sizes(SizeId), total FLOAT NOT NULL)''')
	
	# in progress
	def createToppingPricesTable(self, cursor):
		"""Crea la tabla ToppingPrices si Store.db no existe"""
		cursor.execute('''CREATE TABLE IF NOT EXISTS IngredientPrices 
						(SizeId INTEGER, CONSTRAINT fk_SizeId FOREIGN KEY (SizeId) REFERENCES Sizes(SizedId), 
						ToppingId INTEGER, CONSTRAINT fk_ToppingId FOREIGN KEY (ToppingId) REFERENCES Toppings(ToppingId), 
						price FLOAT NOT NULL)''')
		cursor.execute('''INSERT INTO ToppingPrices (SizeId, ToppingId, price) VALUES (?,?,?)''') # insert multiple rows here (for each ToppingId)
	
	@property
	def instance(self):
		return self.__instance