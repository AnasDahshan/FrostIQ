import sqlite3

class ProductDatabase:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                barcode TEXT UNIQUE,
                name TEXT,
                brand TEXT,
                quantity TEXT,
                energy_100g TEXT,
                energy_unit TEXT,
                nutriscore TEXT,
                bingImage_url TEXT,
                image_url TEXT
            )
        ''')
        self.conn.commit()

    def add_product(self, product_info, barcode):

        # check if the product already exists in the database
        if self.get_product_by_barcode(barcode):
            print(f"Product with barcode {barcode} already exists in database.")
            return

        query = '''
            INSERT OR REPLACE INTO products (
                barcode, name, brand, quantity, energy_100g, energy_unit, nutriscore, bingImage_url, image_url
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        params = (
            barcode,
            product_info['name'],
            product_info['brand'],
            product_info['quantity'],
            product_info['energy_100g'],
            product_info['energy_unit'],
            product_info['nutriscore'],
            product_info['bingImage_url'],
            product_info['image_url']
        )
        self.cursor.execute(query, params)
        self.conn.commit()
        print("Product added to database.")


    def get_all_products(self):
        self.cursor.execute('SELECT * FROM products')
        rows = self.cursor.fetchall()
        products = []
        for row in rows:
            products.append({
                'barcode': row[0],
                'name': row[1],
                'brand': row[2],
                'quantity': row[3],
                'energy_100g': row[4],
                'energy_unit': row[5],
                'nutriscore': row[6],
                'bingImage_url': row[7],
                'image_url': row[8],
            })
        return products


    def get_product_by_barcode(self, barcode):
        # execute a query to retrieve the product by barcode
        query = "SELECT * FROM products WHERE barcode = ?"
        self.cursor.execute(query, (barcode,))
        row = self.cursor.fetchone()

        # return the product as a dictionary, or None if it's not found
        if row is not None:
            return {
                'barcode': row[0],
                'name': row[1],
                'brand': row[2],
                'quantity': row[3],
                'energy_100g': row[4],
                'energy_unit': row[5],
                'nutriscore': row[6],
                'bingImage_url': row[7],
                'image_url': row[8],
            }
        else:
            return None
