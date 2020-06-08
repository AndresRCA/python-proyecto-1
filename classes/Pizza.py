class Pizza:
	"""This class emulates an ordered Pizza"""
	def __init__(self, size, toppings):
		"""Initialize size, base toppings and extra toppings"""
		self.size = size
		self.extra_toppings_list = ['jamon', 'champiñones', 
									'pimenton', 'doble queso',
									'aceitunes', 'pepperoni', 
									'salchichon']
		self.toppings = toppings
		self.toppings.append('salsa de tomate')
		self.toppings.append('queso')

	def pizza_price(self):
		"""Calculates and returns the total price for the pizza"""
		price = 0
		"""Evaluate pizza size"""
		if self.size == 'personal':
			"""Set pizza size price """
			price += 10
			for topping in self.toppings:
				"""Get each topping of the pizza"""
				if topping in self.extra_toppings_list:
					"""
					If topping is an extra search for the extra price 
					and add it to the total price
					"""
					extra_index = self.extra_toppings_list.index(topping)
					if extra_index == 0:
						price += 1.5
					elif extra_index == 1:
						price += 1.75
					elif extra_index == 2:
						price += 1.5
					elif extra_index == 3:
						price += 0.8
					elif extra_index == 4:
						price += 1.8
					elif extra_index == 5:
						price += 1.25
					elif extra_index == 6:
						price += 1.6

		elif self.size == 'mediana':
			"""Set pizza size price"""
			price += 15
			for topping in self.toppings:
				"""Get each topping of the pizza"""
				if topping in self.extra_toppings_list:
					"""
					If topping is an extra search for the extra price 
					and add it to the total price
					"""
					extra_index = self.extra_toppings_list.index(topping)
					if extra_index == 0:
						price += 1.75
					elif extra_index == 1:
						price += 2.05
					elif extra_index == 2:
						price += 1.75
					elif extra_index == 3:
						price += 1.3
					elif extra_index == 4:
						price += 2.15
					elif extra_index == 5:
						price += 1.7
					elif extra_index == 6:
						price += 1.85

		elif self.size == 'familiar':
			price += 20
			"""Set pizza size price"""
			for topping in self.toppings:
				"""Get each topping of the pizza"""
				if topping in self.extra_toppings_list:
					"""
					If topping is an extra search for the extra price 
					and add it to the total price
					"""
					extra_index = self.extra_toppings_list.index(topping)
					if extra_index == 0:
						price += 2
					elif extra_index == 1:
						price += 2.5
					elif extra_index == 2:
						price += 2
					elif extra_index == 3:
						price += 1.7
					elif extra_index == 4:
						price += 2.6
					elif extra_index == 5:
						price += 1.9
					elif extra_index == 6:
						price += 2.1
		"""Resturn´s the final price"""
		return price