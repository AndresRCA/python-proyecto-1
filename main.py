import os 
import glob
from datetime import datetime

from classes.db_model.SQLiteDB import SQLiteDB
from classes.Pizza import Pizza
from classes.Order import Order

def readOrders(pz_file):
	""" 
	Read each '.pz' file in the directory
	returns a list with the orders in each .pz file fill with a list for 
	each order on the .pz file
	"""
	#get each '.pz' file path
	try:		
		# Open each ".pz" file
		with open(pz_file, encoding='utf-8') as file_object:
			lines = file_object.readlines()
			lines = [line.rstrip('\n') for line in lines] # remove trailing new lines

	except FileNotFoundError:
		print(f'{pz_file} Not found.')

	else:
		# Create a list wich has each order in a list inside it
		# [[order1], [order2],...]
		order_n = []
		arranged_orders = []
		for line in lines:
			if line != 'FIN_PEDIDO' and line != 'COMIENZO_PEDIDO':
				order_n.append(line) # fill order
			if line == 'COMIENZO_PEDIDO':
				order_n = [] # create new order
			if line == 'FIN_PEDIDO':
				arranged_orders.append(order_n) # add finished order
		return arranged_orders

def getOrders(arranged_orders):	
	"""Returns a list of Order objects from a list of lines coming from a .pz file"""
	orders = []
	# Separate each propertie from the order
	for order in arranged_orders:
		# Get Name and Date
		customer_name, order_date = order[0].split(';')

		# whenever any of these values is None, the order is cancelled when inserting to the database (due to NOT NULL constraints)
		customer_name = customer_name or None # if customer_name is empty string, assigns None value (see Short Circuit Evaluations)
		
		order_date = order_date or None
		if order_date: # if order_date is set, check format
			try:
				# Check if date is formatted in dd/mm/yyyy
				datetime.strptime(order_date, '%d/%m/%Y')
			except:
				# Not a valid date format
				order_date = None

		pizzas = []
		# Get Pizza size and toppings for each pizza in the order if a topping name is not written correctly it wont be added to the pizza.
		for line in order[1:]:
			size_toppings = line.split(';')
			size = size_toppings[0]
			toppings = size_toppings[1:]
			pizza = Pizza(size, toppings)
			pizzas.append(pizza)
			total = pizza.get_total_price()
			print('Client:', customer_name)
			print('Date:', order_date)
			print('Size:', size)
			print('Toppings:', toppings)
			print('Total:', total)
			print('')
		orders.append(Order(customer_name, order_date, pizzas))
	return orders
		
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
			f.write('{:20} {} {:25.2f}\n'.format(sale['name'].capitalize(), sale['Unidades'], sale['Monto_Ums']))
	#final line
	f.write('===========================================')
	f.close()
		
if __name__ == '__main__':
	# main start
	while(1):
		print('1.{:20} 2.{}\n3.{:20}'.format('Cargar ordenes', 'Generar resumen', 'Salir'))
		choice = int(input())
		if choice == 1:			
			pz_files = glob.glob('./orders/*.pz') # get every .pz file
			for pz_file in pz_files:
				# process orders in each file
				print('\ninfo in {}:\n'.format(pz_file))
				arranged_orders = readOrders(pz_file)
				print(arranged_orders, '\n')
				orders = getOrders(arranged_orders)
				db = SQLiteDB.getInstance()
				for order in orders:
					db.insertFullOrder(order)
			print('Ordenes procesadas e insertadas en la base de datos de manera exitosa\n')
		elif choice == 2:
			# generate a summary
			createSummaryFile()
			print('\nResumen generado en summary/summary.txt\n')
		elif choice == 3:
			break
		else:
			print('ingrese una opción valida')