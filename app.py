# This is where I learned to remove the dollar sign ($) from the prices when cleaning up the data: https://builtin.com/software-engineering-perspectives/python-remove-character-from-string
# This is where I learned to join both tables together in order to query the brand's table to get a brand's name using its ID: https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_working_with_joins.htm
from models import (Brands, session, Base, Product, engine)
import csv
import datetime

def clean_quantity(quant):
    try:
        price_quantity = int(quant)
    except ValueError:
        input('''
                \nPlease enter a number.
                \rPress enter to try again.
            ''')
        return
    else:
        return price_quantity

def clean_price(price_str):
    try:
        price_string = price_str.strip("$")
        price_float = float(price_string)
    except ValueError:
        input('''
                \nPlease enter a price.
                \rEx: 10.65 or $10.65
                \rPress enter to try again.
            ''')
        return
    else:
        price_in_cents = int(price_float * 100)
        return price_in_cents

def clean_date(date_str):
    split_date = date_str.split('/')
    try:
        month = int(split_date[0])
        day = int(split_date[1])
        year = int(split_date[2])
        return_date = datetime.date(year, month, day)
    except ValueError:
        input('''
                \nThe date should be in the following format:
                \rMonth-Day-Year
                \rEx: 5/19/2023
                \r Press enter to try again.
            ''')
        return
    except IndexError:
        input('''
                \nThe date should be in the following format:
                \rMonth-Day-Year
                \rEx: 5/19/2023
                \r Press enter to try again.
            ''')
        return
    else:
        return return_date

def clean_id(id_str, id_options):
    try:
        id = int(id_str) 
    except ValueError:
        input("The ID must be an integer. Press enter and try again.")
        return
    else:
        if id in id_options:
            return id
        else:
            input("The integer that you typed in is out of the range. Press enter and try again.")
            return


def add_csv():
    with open('brands.csv') as csvfile:
        data = csv.reader(csvfile)
        rows = list(data)
        for brand_row in rows[1:]:
            brand_in_db = session.query(Brands).filter(Brands.brand_name==brand_row[0]).one_or_none()
            if brand_in_db == None:
                brand_name = brand_row[0]
                new_brand = Brands(brand_name=brand_name)
                session.add(new_brand)
            session.commit()

    with open('inventory.csv') as csvfile2:
        data = csv.reader(csvfile2)
        rows = list(data)
        for inventory_row in rows[1:]:
            product_in_db = session.query(Product).filter(Product.product_name==inventory_row[0]).one_or_none()
            if product_in_db == None:
                product_name = inventory_row[0]
                product_price = clean_price(inventory_row[1])
                product_quantity = inventory_row[2]
                date_updated = clean_date(inventory_row[3])
                brand_id = session.query(Brands.id).filter(Brands.brand_name==inventory_row[4])
                new_product = Product(product_name=product_name, product_price=product_price, product_quantity=product_quantity, date_updated=date_updated, brand_id=brand_id)
                session.add(new_product)
        session.commit()
            
def app():
    print('''Welcome to the Grocery Shopping Inventory App!
            \nChoose one of the following options:
            \nView a single product's inventory (V)
            \rAdd a new product to the database (N)
            \rView an analysis (A)
            \rMake a backup of the entire inventory (B)
        ''')
    
    menu_input = input('What would you like to do? ')
    
    while menu_input.lower() != 'v' and menu_input.lower() != 'n' and menu_input.lower() != 'a' and menu_input.lower() != 'b':
        menu_input = input("Sorry, I don't understand. Please type 'v', 'n', 'a' or 'b'. ")

    if menu_input.lower() == 'v':
        # Displaying a product by ID
        id_options = []

        for product in session.query(Product):
            id_options.append(product.id)
        id_error = True
        while id_error:
            id_choice = input(f'''
                    \nID Options: {id_options} 
                    \rBook ID: ''')
            id_choice = clean_id(id_choice, id_options)
            if type(id_choice) == int:
                id_error = False
        the_product = session.query(Product).filter(Product.id==id_choice).first()
        print(f'''
                \nProduct Name: {the_product.product_name}
                \rPrice: {the_product.product_price}
                \rQuantity: {the_product.product_quantity}
                \rDate Updated: {the_product.date_updated}
                \rBrand: {the_product.brand_id}
                ''')
        input('Press enter to return to the main menu. ')
        app()

    if menu_input.lower() == 'n':
        # Add new product to database
        product_name = input('Product Name: ')
        price_error = True
        while price_error:
            product_price = input('Price (Ex: 16.73): ')
            product_price_cleaned = clean_price(product_price)
            if type(product_price_cleaned) == int:
                price_error = False
        quantity_error = True
        while quantity_error:
            product_quantity = input('Quantity: ')
            product_quantity_cleaned = clean_quantity(product_quantity)
            if type(product_quantity_cleaned) == int:
                quantity_error = False
        date_error = True
        while date_error:
            date_updated = input('Date updated (Ex: 1/20/2023): ')
            date_updated_cleaned = clean_date(date_updated)
            if type(date_updated_cleaned) == datetime.date:
                date_error = False
        brand_name_input = input('Brand: ')
        brand_name_in_db = session.query(Brands).filter(Brands.brand_name==brand_name_input).one_or_none()
        if brand_name_in_db == None:
            new_brand = Brands(brand_name=brand_name_input)
            session.add(new_brand)
            session.commit()
            brand_name = session.query(Brands).filter(Brands.brand_name==brand_name_input).first().id
        else:    
            brand_name = brand_name_in_db.id
        new_product = Product(product_name=product_name, product_price=product_price_cleaned, product_quantity=product_quantity_cleaned, date_updated=date_updated_cleaned, brand_id=brand_name)
        session.add(new_product)
        session.commit()
        input('Product added. Press enter to continue.')
        app()

    if menu_input.lower() == 'a':
        with open('inventory.csv') as csvfile2:
            data = csv.reader(csvfile2)
            rows = list(data)
            for inventory_row in rows[1:]:
                brand_name = session.query(Brands.brand_name).filter(Brands.brand_name==inventory_row[4])
        # Analyze the database
            most_expensive_item = session.query(Product.product_name).order_by(Product.product_price.desc()).first()
            least_expensive_item = session.query(Product.product_name).order_by(Product.product_price).first()
            brand_most_products = session.query(Brands.brand_name).join(Product).order_by(Product.product_name).first()
            product_with_highest_quantity = session.query(Product.product_name).order_by(Product.product_quantity.desc()).first()
            total_products = session.query(Product).count()
            print(f'''Most Expensive Item: {most_expensive_item}''')
            print(f'''Least Expensive Item: {least_expensive_item}''')
            print(f'''Brand with most products: {brand_most_products}''')
            print(f'''Product with highest quantity in stock: {product_with_highest_quantity}''')
            print(f'''Total number of product types: {total_products}''')
            input('Press enter to return to the main menu. ')
        app()

    if menu_input.lower() == 'b':
        # Back up the database
        def create_backup():
            header = ['Product ID', 'Product Name', 'Product Price', 'Product Quantity', 'Date Updated', 'Brand']
            header_2 = ['Brand ID', 'Brand Name']
            info = session.query(Product.id, Product.product_name, Product.product_price, Product.product_quantity, Product.date_updated, Product.brand_id)
            info_2 = session.query(Brands.id, Brands.brand_name)

            with open('backup_inventory.csv', 'w') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                for row in info:
                    writer.writerow(row)         

            with open('backup_brands.csv', 'w') as f:
                writer = csv.writer(f)
                writer.writerow(header_2)
                for row_2 in info_2:
                    writer.writerow(row_2)
        create_backup()

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    add_csv()
    app()