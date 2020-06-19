from classes.db_model.SQLiteDB import SQLiteDB

class Pizza:
	"""This class emulates an ordered Pizza"""
	def __init__(self, size, toppings):
		"""Initialize size and extra toppings"""
		self.size = self.getSizeId(size)
		self.toppings = self.get_toppings_id(toppings)

	def getSizeId(self, size_name):
		db = SQLiteDB.getInstance()
		sizeId = db.getSizeIdByName(size_name)
		return sizeId
		
	def get_toppings_id(self, toppings):
		"""Return the topping´s id."""
		db = SQLiteDB.getInstance()
		toppings_id = db.get_toppings_rows()
		ids = []
		"""Evaluate pizza toppings"""
		for topping in toppings:
			for row in toppings_id:
				if topping == row[1]:
					ids.append(row[0])
		return ids
		
	def get_size_price(self):
		"""
		From pizza size get id, size, price from db
		Returns size id, price.
		"""
		db = SQLiteDB.getInstance()
		size_price = db.getSizePriceById(self.size)
		return size_price
		
	def get_toppings_price(self):
		"""
		From ToppingId and SizeId calculate the total price of toppings
		"""
		topping_price = 0
		db = SQLiteDB.getInstance()
		for toppingId in self.toppings:
			topping_price += db.getToppingPrice(self.size, toppingId)
		return topping_price
	
	def get_total_price(self):
		"""Calculates the final price for the pizza"""
		size_price = self.get_size_price()
		toppings_price = self.get_toppings_price()
		total = size_price + toppings_price
		total = '{:.2f}'.format(total)
		return float(total)
		

				
