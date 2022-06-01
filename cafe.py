from dataclasses import dataclass
from unittest.util import strclass
from PySide6.QtWidgets import *
from PySide6.QtGui import QPixmap
import os

# add product, product_list classes
@dataclass
class Product:
    _name: str
    _price: float
    _has_sugar: bool
    _v_option: bool # vegan
    _vg_option: bool # vegetarian

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        if new_name:
            self._name = new_name
        else:
            ValueError()

    @property
    def price(self) -> float:
        return self._price
    
    @price.setter
    def price(self, new_price: float):
        if new_price > 0:
            self._price = new_price
        else:
            ValueError()
    
    @property
    def has_sugar(self) -> bool:
        return self._has_sugar
    
    @has_sugar.setter
    def has_sugar(self, new_has_sugar: bool):
        self._has_sugar = new_has_sugar
    
    @property
    def v_option(self) -> bool:
        return self._v_option
    
    @v_option.setter
    def v_option(self, new_v_option: bool):
        self._v_option = new_v_option
    
    @property
    def vg_option(self) -> bool:
        return self._vg_option
    
    @vg_option.setter
    def vg_option(self, new_vg_option: bool):
        self._vg_option = new_vg_option

@dataclass
class ProductCategory:
    _products: list

    @property
    def products(self) -> list:
        return self._products
    
    @products.setter
    def products(self, new_products:list):
        if len(new_products) > 0:
            self._products = new_products
        else:
            ValueError()
    
    # convert list of products 2 list of names
    @property
    def product_names(self) -> list:
        product_names = [product.name for product in self._products]

        return product_names

@dataclass
class Specials(Product):
    _day: str
    _origin: str

    @property
    def day(self) -> str:
        return self._day
    
    @day.setter
    def day(self, new_day: str):
        if new_day: # if its str input > 0
            self._day = new_day
        else:
            raise ValueError()

    @property
    def origin(self) -> str:
        return self._origin
    
    @origin.setter
    def origin(self, new_origin: str):
        if new_origin:
            self._origin = new_origin
        else:
            raise ValueError()
@dataclass
class Order():
    _product_names: list
    _total_price: float
    _day: str

    @property
    def product_names(self) -> list:
        return self._product_names

    @product_names.setter
    def product_names(self, new_product_names: list):
        self.product_names = new_product_names
    
    @property
    def total_price(self) -> float:
        return self._total_price
    
    @total_price.setter
    def total_price(self, new_total_price: float):
        self.total_price = new_total_price

    @property
    def day(self) -> str:
        return self._day
    
    @day.setter
    def day(self, new_day: str):
        self.day = new_day

# create empty order
order = Order([], 0.0, '')

# add each group (sandwiches, sushi, drinks, specials) + lsit of names
sandwiches_category = ProductCategory([
    Product('Chicken Mayo Sandwich', 3.50, True, False, False),
    Product('Egg Sandwich', 3.00, False, False, True),
    Product('Beef Sandwich', 3.80, False, False, False),
    Product('Tempeh Sandwich', 3.50, False, True, True), 
    Product('PBJ', 3.00, True, True, True)
])

sushi_category = ProductCategory([
    Product('Chicken (3pc)', 4.50, False, False, False),
    Product('Salmon (3pc)', 4.50, False, False, False),
    Product('Avocado (3pc)', 4.80, False, True, True),
    Product('Chicken Rice Bowl', 5.50, False, False, False),
    Product('Vegetarian Rice Bowl', 5.50, False, False, True)
])

drinks_category = ProductCategory([
    Product('Soda Can', 2.00, True, True, True),
    Product('Aloe Vera Drink', 3.50, True, False, True),
    Product('Chocolate Meat Milk', 3.50, True, False, False),
    Product('Water Bottle', 2.50, False, True, True),
    Product('Instant Hot Chocolate', 1.50, True, False, True)
])

specials_category = ProductCategory([
    Specials('Kale Moa', 6.00, True, False, False, 'Monday'),
    Specials('Potjiekos', 6.00, False, False, False, 'Tuesday'),
    Specials('Hangi', 6.00, False, True, True, 'Wednesday', 'Aotearoa'),
    Specials('Paneer Tikka Masala', 6.00, False, False, True, 'Thursday'),
    Specials('Chow Mein', 6.00, False, True, True, 'Friday')
])

# set up app
app = QApplication()
main_window = QMainWindow()
main_window.setWindowTitle('KAI UI')
main_window.resize(640, 480)

central_widget = QWidget()
main_window.setCentralWidget(central_widget)
main_hbox = QHBoxLayout()
central_widget.setLayout(main_hbox)

left_widget = QWidget() # widget where all the product lists is
left_v_layout = QVBoxLayout()
left_widget.setLayout(left_v_layout)

# add day selection + master list
school_days = [
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday'
]

day_select = QComboBox()
day_select.addItems(x for x in school_days)

left_v_layout.addWidget(QLabel('Select Day:'))
left_v_layout.addWidget(day_select)

# add main list selection widget
find_categories = [ # list ver because couldn't use dict in index change
    'Sandwiches',
    'Sushi',
    'Drinks',
    'Today\'s Special'
]

categories_dict = { # dict version of ^ to move thru
    'Sandwiches': sandwiches_category,
    'Sushi': sushi_category,
    'Drinks': drinks_category,
    'Today\'s Special': specials_category
}

# add category selection
select_category = QComboBox()
select_category.addItems(x for x in find_categories)

left_v_layout.addWidget(QLabel('Select Category:'))
left_v_layout.addWidget(select_category)

# add product list widgets, add to order button
products_select = QListWidget()
add_to_order = QPushButton('Add item to order')

left_v_layout.addWidget(products_select)
left_v_layout.addWidget(add_to_order)
main_hbox.addWidget(left_widget)

# right widget 4 product details
right_widget = QWidget()
right_v_layout = QVBoxLayout()
right_widget.setLayout(right_v_layout)

# add price, vegan/vegetarian, sugarfree etc.
deets = QWidget()
deets_v_layout = QVBoxLayout()

price_label = QLabel('')
deets_label = QLabel('')
deets_v_layout.addWidget(price_label)
deets_v_layout.addWidget(deets_label)

deets.setLayout(deets_v_layout)

# submit order button
submit_order = QPushButton('Submit order')

right_v_layout.addWidget(deets)
right_v_layout.addWidget(submit_order)

main_hbox.addWidget(right_widget)

# set category, product index @ 0
selected_category = find_categories[0]
selected_product = 0
selected_day = 0

# add day changed reaction
def day_select_currentIndexChanged(index: int):
    ''' changes global day variable - user can only order special items
        if its available day matches index 
    '''
    global selected_day
    selected_day = school_days[index]


# add category changed reaction
def select_category_currentIndexChanged(index: int):
    ''' changes list widget 2 selected category (e.g. sushi) '''
    global selected_category
    selected_category = find_categories[index]

    # add product names to list widget??!! + clear first
    products_select.clear()
    products_select.addItems(x for x in categories_dict[selected_category].product_names)


# add product changed (list widget) reaction
def products_select_currentRowChanged(row: int):
    ''' changes product details (price etc.) based on product selected '''
    global selected_product

    # get list of products in category (to ID index)
    product_names = categories_dict[selected_category].product_names

    # get product selected on list, find index
    product = product_names[row]

    selected_product = product_names.index(product)

    # get list of product objects + plug index in - find deets of product selected
    products = categories_dict[selected_category].products
    product = products[selected_product]

    # change labels
    price_label.setText('Price: ${:.2f}'.format(product.price))
    string = ''
    
    if product.has_sugar == True:
        string += 'This item contains sugar.\n'
    else:
        string += 'This item is Sugarfree.\n'
    
    if product.v_option == True:
        string += 'This item is Vegan!\n'
    elif product.vg_option == True:
        string += 'This item is Vegetarian!\n'
    else:
        string += 'This item contains meat.\n'

    # check if need 2 display day of week label
    if categories_dict[selected_category] == categories_dict['Today\'s Special']:
        string += 'Only available on {}s.\n'.format(product.day)
        string += 'Country of origin: {}\n'.format(product.origin)
    
    # change label w/ string created
    deets_label.setText(string)


def add_to_order_clicked(checked: bool):
    ''' adds selected item to order when clicked '''
    # add item selected to order
    products = categories_dict[selected_category].products
    product = products[selected_product]
    
    # check if item is in specials category
    if product in specials_category.products:
        # check if product day + selected day match
        if product.day == selected_day:
            order.product_names.append(product.name)
            print(product.day)
            print(product.price)
            print(order)
            QMessageBox(QMessageBox.Icon.Information, 'Item Added', 
            product.name + ' has been added to your order.').exec()

        elif product.day != selected_day:
            QMessageBox(QMessageBox.Icon.Information, 'Error', '{} isn\'t available on {}s.'.format(
                product.name, selected_day
            )).exec()

    # add 2 order if OK
    else:
        order.product_names.append(product.name)
        print(product.price)
        print(order)

        QMessageBox(QMessageBox.Icon.Information, 'Item Added', 
        product.name + ' has been added to your order.').exec()


# manually set selection to i=0 so isn't empty yas
# also connect event
day_select_currentIndexChanged(0)
day_select.currentIndexChanged.connect(day_select_currentIndexChanged)

# same to other widgets
select_category_currentIndexChanged(0)
select_category.currentIndexChanged.connect(select_category_currentIndexChanged)

products_select_currentRowChanged(0)
products_select.currentRowChanged.connect(products_select_currentRowChanged)

# let items be added 2 order
add_to_order.clicked.connect(add_to_order_clicked)

# run app
main_window.show()
app.exec()