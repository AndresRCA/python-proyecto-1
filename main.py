import os 

from classes.db_model.SQLiteDB import SQLiteDB
from classes.Pizza import Pizza
from classes.Order import Order

def accesing_pz_files(files_directory):
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

def get_info(pz_files):
	""" 
	Read each '.pz' file in the directory
	returns a list with the orders in each .pz file fill with a list for 
	each order on the .pz file
	"""
	# Check if file is not in the directory
	
	#get each '.pz' file 
	orders = []
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
		orders.append(arrange_orders)
	return orders

def work_the_order(arrange_orders):	
	""" 
	Analyze each parameter for each order
	and calculate. 
	"""
	# Separate each propertie from the order
	for order in arrange_orders:
		# Get Name and Date
		name_date = order[1].split(';')
		customer_name = name_date[0]
		order_date = name_date[1]
		customer_name = customer_name.replace('\n', '') #Erase trash 
		order_date = order_date.replace('\n', '') #Erase trash 
		print(order_date)
		print(customer_name)

		# Get Pizza size and toppings for each pizza in the order
		for line in order[2:-1]:
			if line != 'FIN_PEDIDO\n':
				size_toppings = line.split(';')
				size = size_toppings[0]
				toppings = size_toppings[1:]
				size = size.replace('\n', '') #Erase trash 
				toppings = [s.strip('\n') for s in toppings] #Erase trash 
			price = Pizza(size, toppings)
			size_id, size_price = price.get_size_price()
			toppings_id = price.get_toppings_id(size_id)
			toppings_price = price.get_toppings_price(toppings_id, size_id)
			total = price.get_total_price(float(size_price), float(toppings_price))
			print('Size:')
			print(size)
			print('toppings:')
			print(toppings)
			print('SizeIdD:')
			print(size_id)
			print('SizePrice:')
			print(size_price)
			print('ToppingsID:')
			print(toppings_id)
			print('ToppingsPrice:')
			print(toppings_price)
			print('Total:')
			print(total)
			print('') 
		
def createSummaryFile():
	if not os.path.exists('./summary'):
		os.makedirs('./summary')
	f = open('./summary/summary.txt', 'w')
	db = SQLiteDB.getInstance()
	dates = db.getOrderDates()
	for date in dates:
		# separation line
		f.write('===========================================\n')
		
		f.write('Fecha: '+str(date['order_date'])+'\n')
		
		orders_total = db.getOrdersTotal(date['order_date'])
		f.write('Venta Total: '+str(orders_total)+' UMs\n')
		
		# ventas por pizza
		sales_pizza = db.getSalesByPizza(date['order_date']) # at this point it's impossible that this list is empty
		f.write('Ventas por pizza (sin incluir adicionales):\n')
		f.write('{:20} {:20} {:22}\n'.format('Tamaño', 'Unidades', 'Monto Ums'))
		for sale in sales_pizza:
			f.write('{:20} {} {:25}\n'.format(sale['name'].capitalize(), sale['Unidades'], sale['Monto_Ums']))
		
		# ventas por ingrediente
		sales_topping = db.getSalesByTopping(date['order_date'])
		f.write('\nVentas por Ingrediente:\n')
		f.write('{:20} {:20} {:22}\n'.format('Ingredientes', 'Unidades', 'Monto Ums'))
		for sale in sales_topping:
			f.write('{:20} {} {:25}\n'.format(sale['name'].capitalize(), sale['Unidades'], sale['Monto_Ums']))
	f.close()
		
if __name__ == '__main__':
	# main start
	while(1):
		print('1.{:20} 2.{}\n3.{:20}'.format('Cargar ordenes', 'Generar resumen', 'Salir'))
		choice = int(input())
		if choice == 1:
			# process orders
			files_directory = './orders'
			pz_files = accesing_pz_files(files_directory)
			arrange_orders = get_info(pz_files)
			print(arrange_orders)
			for each_pz in arrange_orders:
				"""separate each .pz file"""
				print('info in .pz:')
				print(each_pz)
				work_the_order(each_pz)
			print('Ordenes procesadas e insertadas en la base de datos de manera exitosa')
		elif choice == 2:
			# generate a summary
			createSummaryFile()
			print('Resumen generado en summary/summary.txt')
		elif choice == 3:
			break
		else:
			print('ingrese una opción valida')