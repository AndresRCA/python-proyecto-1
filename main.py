import os 

from classes.db_model.SQLiteDB import SQLiteDB
from classes.Pizza import Pizza
from classes.Order import Order

def accesing_files(files_directory):
	"""
	Accesing to the files in the "orders" directory and returning a 
	list with the name of each '.pz' file.
	"""
	files_in_directory = os.listdir(files_directory)
	pz_files = []

	# Getting the ".pz" files only and creating a list from these ".pz" files.
	for each_file in files_in_directory:
		if each_file[-3:] == '.pz':
			pz_files.append(each_file)
	return pz_files

def getting_info(pz_files):
	""" Read each '.pz' file in the directory and print the price"""
	# Check if file is not in the directory
	
	#get each '.pz' file 
	for pz_file in pz_files:
		# Get directoryfor each ".pz" directory
		pz_file_direction = f'{files_directory}/{pz_file}'
		try:		
			# Open each ".pz" file
			with open(pz_file_direction, encoding='utf-8') as file_object:
				lines = file_object.readlines()

		except FileNotFoundError:
			print(f'{pz_file} Not found.')

		else:
			# Create a list wich has each order in a list inside it
			# [[order1], [order2],...]
			order_n = []
			arrange_orders = []
			for line in lines:
				if line != 'FIN_PEDIDO\n':
					order_n.append(line)
				if line == 'FIN_PEDIDO\n':
					order_n.append(line)
					arrange_orders.append(order_n)
					order_n = []
		
			# Separate each propertie from the order
			for order in arrange_orders:
				# Get Name and Date
				name_date = order[1].split(';')
				customer_name = name_date[0]
				order_date = name_date[1]
				customer_name = customer_name.replace('\n', '') #Erase trash 
				order_date = order_date.replace('\n', '') #Erase trash 
				# Get Pizza size and toppings for each pizza in the order
				aux = []
				pizzas_in_order = []
				for line in order[2:-1]:
					if line != 'FIN_PEDIDO\n':
						size_toppings = line.split(';')
						size = size_toppings[0]
						toppings = size_toppings[1:]
					size = size.replace('\n', '') #Erase trash 
					toppings = [s.strip('\n') for s in toppings] #Erase trash 
					price = Pizza(size, toppings)
					print(size)
					print(toppings)
					print(price.pizza_price())
					print('')
					aux.append(size)
					aux.append(toppings)
					pizzas_in_order.append(aux)
					aux = []		

if __name__ == '__main__':
	# main start
	
	files_directory = 'C:/Users/Administrador/Desktop/UCAB/10mo/Python/Proyectos/Proyecto1/python-proyecto-1/orders'
	pz_files = accesing_files(files_directory)
	getting_info(pz_files)	