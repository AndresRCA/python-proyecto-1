class Order:
	
	def __init__(self, name, date, pizzas):
		self.name = name
		self.date = date
		self.pizzas = pizzas
		
	def getTotal(self):
		total = 0
		for pizza in self.pizzas:
			total += pizza.get_total_price()
		return total