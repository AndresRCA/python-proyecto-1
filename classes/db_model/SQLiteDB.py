from os import path
from classes.db_model.enums.Toppings import Toppings
from classes.db_model.enums.Sizes import Sizes
import sqlite3

class SQLiteDB:
	"""SQLiteDB es una clase Singleton que maneja la base de datos y sus operaciones"""
	
	__instance = None
	
	# fixed values stored in database (needed for creating the database), should get extracted and not initialized when db is already up
	__size_ids = (Sizes.PERSONAL, Sizes.MEDIUM, Sizes.FAMILY)
	__size_names = ('personal', 'mediana', 'familiar')
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
		"""establece el objeto y crea una conexión"""
		
		if SQLiteDB.__instance != None:
			raise Exception('Esta clase es un singleton')
		else:
			SQLiteDB.__instance = self
			self.connection = self.setUp()
			
	def setUp(self):
		"""Crea DB e inicialización. Retorna la conexión"""
		
		if path.exists('./DB/Store.db'):
			db = sqlite3.connect('./DB/Store.db')
			cursor = db.cursor()
			cursor.execute('PRAGMA foreign_keys=1') # enforce foreign keys
			db.commit()
			db.row_factory = sqlite3.Row # important setting, this way rows can be accessed through column names plus other functionality
			return db
		db = sqlite3.connect('./DB/Store.db')
		db.row_factory = sqlite3.Row # important setting, this way rows can be accessed through column names plus other functionality
		cursor = db.cursor()
		
		#cursor.execute('SET CHARACTER utf8')
		# create every table in the DB
		self.initSizesTable(cursor)
		self.initToppingsTable(cursor)
		self.initOrdersTable(cursor)
		self.initPizzasTable(cursor)
		self.initPizzaTopping(cursor)
		self.initToppingPricesTable(cursor)
		cursor.execute('PRAGMA foreign_keys=1') # enforce foreign keys
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
		# get the ToppingPrices rows to insert into table
		values = [(price, size_id.value, topping.value) for topping in Toppings for size_id, price in zip(self.__size_ids, self.__topping_prices[topping.value])]
		cursor.executemany('INSERT INTO ToppingPrices (price, SizeId, ToppingId) VALUES (?,?,?)', values) # insert multiple rows here (for each ToppingId)
	
	def getToppingPrice(self, sizeId, toppingId):
		"""Retorna el precio de un ingrediente dependiendo del tamaño"""
		
		price = None
		try:			
			c = self.connection.cursor()
			
			c.execute('SELECT price FROM ToppingPrices WHERE SizeId = {} AND ToppingId = {}'.format(sizeId, toppingId))
			price = c.fetchall()
			if price:
				price = price[0]['price']
		except sqlite3.Error as e:
			print("Error reading data from SQLite table:", e)
		finally:
			return price
	
	def getOrderDates(self):
		"""Retorna fechas unicas dentro de la tabla Orders"""
		
		dates = []
		try:			
			c = self.connection.cursor()
			c.execute('SELECT DISTINCT order_date FROM Orders ORDER BY order_date')
			dates = c.fetchall()
		except sqlite3.Error as e:
			print("Error reading data from SQLite table:", e)
		finally:
			return dates
	
	def getOrdersTotal(self, date = None):
		"""Retorna el total de las ventas"""
		
		total = None
		try:			
			c = self.connection.cursor()
			
			where_clause = "WHERE order_date = '{}'".format(date) if date else ''
			c.execute('SELECT SUM(total) as total FROM Orders '+where_clause+' ORDER BY order_date')
			total = c.fetchall()
			if total:
				total = total[0]['total']
		except sqlite3.Error as e:
			print("Error reading data from SQLite table:", e)
		finally:
			return total
	
	def getSalesByPizza(self, date = None):
		"""Retorna ventas por tamaño de pizza"""
		
		sales = []
		try:			
			c = self.connection.cursor()
			
			where_clause = "WHERE O.order_date = '{}'".format(date) if date else ''
			sql_query = '''SELECT S.SizeId, S.name, COUNT(P.PizzaId) as Unidades, IFNULL(SUM(S.price), 0.00) as Monto_UMs 
			FROM Sizes S
			LEFT JOIN  Pizzas P on P.SizeId = S.SizeId 
			LEFT JOIN Orders O on O.OrderId = P.OrderId '''+where_clause+''' GROUP BY S.SizeId'''
			
			c.execute(sql_query)
			sales = c.fetchall()
		except sqlite3.Error as e:
			print("Error reading data from SQLite table:", e)
		finally:
			return sales
	
	def getSalesByTopping(self, date = None):
		"""Retorna ventas por toppings"""
		
		sales = []
		try:			
			c = self.connection.cursor()
			
			where_clause = "WHERE O.order_date = '{}'".format(date) if date else ''
			sql_query = '''SELECT T.ToppingId, T.name, COUNT(PT.ToppingId) as Unidades, IFNULL(SUM(TP.price), 0.00) as Monto_UMs 
			FROM Toppings T 
			LEFT JOIN PizzaTopping PT on PT.ToppingId = T.ToppingId 
			LEFT JOIN Pizzas P on P.PizzaId = PT.PizzaId 
			LEFT JOIN Sizes S on S.SizeId = P.SizeId 
			LEFT JOIN ToppingPrices TP on TP.SizeId = S.SizeId AND TP.ToppingId = T.ToppingId 
			LEFT JOIN Orders O on O.OrderId = P.OrderId '''+where_clause+''' GROUP BY T.ToppingId'''
			
			c.execute(sql_query)
			sales = c.fetchall()
		except sqlite3.Error as e:
			print("Error reading data from SQLite table:", e)
		finally:
			return sales
		
	def getSizeIdByName(self, size_name):
		"""Retorna el SizeId dependiendo del parametro 'size_name' de tipo string dado"""
		
		sizeId = None
		try:			
			c = self.connection.cursor()
			
			c.execute("SELECT SizeId FROM Sizes WHERE name = '{}'".format(size_name))
			sizeId = c.fetchall()
			if sizeId:
				sizeId = sizeId[0]['SizeId']
			else:
				sizeId = None
		except sqlite3.Error as e:
			print("Error reading data from SQLite table:", e)
		finally:
			return sizeId
	
	def getSizePriceById(self, sizeId):
		"""Get size price from database"""
		
		price = None
		try:
			cursor = self.connection.cursor()
			cursor.execute("SELECT price FROM Sizes WHERE SizeId = {}".format(sizeId))
			price = cursor.fetchall()
			if price:
				price = price[0]['price']
		except sqlite3.Error as e:
			print("Error reading data from SQLite table:", e)
		finally:
			return price
	
	def get_toppings_rows(self):
		"""Return topping rows"""
		
		rows = []
		try:
			cursor = self.connection.cursor()
			cursor.execute("SELECT * FROM Toppings")
			rows = cursor.fetchall()
		except slqite3.Error as e:
			print("Error reading data from SQLite table:", e)
		finally:
			return rows
	
	def insertFullOrder(self, order):
		"""Inserta orden, pizza y toppings asociados, en sucesion a la base de datos"""
		
		try:
			c = self.connection.cursor()
			c.execute("INSERT INTO Orders (client_name, order_date, total) VALUES (?,?,?)", (order.name, order.date, order.getTotal()))
			
			orderId = c.lastrowid
			for pizza in order.pizzas:
				c.execute("INSERT INTO Pizzas (total, SizeId, OrderId) VALUES (?,?,?)", (pizza.get_total_price(), pizza.size, orderId))
				
				pizzaId = c.lastrowid
				for topping in pizza.toppings:
					c.execute("INSERT INTO PizzaTopping (PizzaId, ToppingId) VALUES (?,?)", (pizzaId, topping))
				
				self.connection.commit() # at this point a pizza in the order is saved	
		except sqlite3.Error as e:
			print("Error inserting data to SQLite table:", e)
		else:
			self.connection.commit() # if there were no errors save changes