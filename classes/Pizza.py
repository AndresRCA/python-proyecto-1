from classes.db_model.SQLiteDB import SQLiteDB

class Pizza:
	"""This class emulates an ordered Pizza"""
	def __init__(self, size, toppings):
		"""Initialize size, base toppings and extra toppings"""
		self.size = size
		self.toppings = toppings
		toppings.append('salsa de tomate')
		toppings.append('queso')

	def get_size_price(self):
		"""
		From pizza size get id, size, price from db
		Returns size id, price.
		"""
		size_price = 0
		db = SQLiteDB.getInstance()
		sizes_info = db.get_sizes_rows()

		"""Evaluate pizza size"""
		for row in sizes_info:
			if self.size == row[1]:
				size_price += row[2]
				size_id = row[0]

		"""Return´s the size id, price"""
		size_price = '{:.2f}'.format(size_price)
		return size_id, size_price
		
	def get_toppings_id(self, size_id):
		"""Return the topping´s id."""
		db = SQLiteDB.getInstance()
		toppings_id = db.get_toppings_rows()
		ids = []
		
		"""Evaluate pizza toppings"""
		for topping in self.toppings:
			for row in toppings_id:
				if topping == row[1]:
					ids.append(row[0])
				
		return ids
		
		
	def get_toppings_price(self, toppings_id, size_id):
		"""
		From toppings ID calculate the total price of toppings
		"""
		topping_price = 0
		db = SQLiteDB.getInstance()
		toppings_info = db.getToppingPricesRows()
		for id in toppings_id:
			for row in toppings_info:
				if size_id == row[1] and id == row[2]:
					topping_price += row[0]

		"""Return´s the toppings final price"""
		topping_price = '{:.2f}'.format(topping_price)
		return topping_price
	
	def get_total_price(self, size_price, topping_price):
		"""Calculates the final price for the pizza"""
		final_price = size_price + topping_price
		final_price = '{:.2f}'.format(final_price)
		return final_price
		

				
