from faker import Faker
from PIL import Image
import os
from glob import glob
import random
import shutil,time


class DataCreator:
	def __init__(self):
		self.parent_dir = os.getcwd().replace('\\', '/')
		self.product_folder = 'products'
		# self.product_folder = 'test/products' # For testing purpose
		self.image_folder = '/images'
		self.product_img_folder = self.product_folder + '/images/products'

		self.data_count = 0
		self.num_of_product = 50
		self.brands = ['Apple', 'Tesla', 'Microsoft',
							'Nike', 'Himel Bikon', 'Facebook']

		self.products = ''
		self.existing_image_names = []


	def create_folder(self, folder):
		if not os.path.exists(folder):
			os.makedirs(folder)
			print(f'--> "{folder}" created successfully!')

	def delete_folder(self,folder):
		if os.path.exists(folder):
			shutil.rmtree(folder)
			print(f'--> "{folder}" removed successfully!')

	def resize_img(self, image_path, width, height):
		img = Image.open(image_path)
		size = (width, height)
		img = img.resize(size)
		img.save(image_path)

	def set_img(self):
		path = 'images'

		image_list = glob('images/*.jpg') + glob('images/*.png') + glob('images/*.jpeg')

		image = random.choice(image_list).replace('\\', '/')

		strings = 'ZXCVBNMLKJHGFDSAQWERTYUIOP0123456789'
		image_name =  f'{self.product_img_folder}/{"".join([random.choice(strings) for _ in range(15)])}.jpg'

		if image_name in self.existing_image_names:
			self.set_img()
		else:
			shutil.copyfile(image, image_name)

			self.existing_image_names.append(image_name)
			self.resize_img(image_name, 500, 300)

			return '/images/products/' + image_name.split('/')[-1]

	def create_product(self):
		product = {
            'name': self.faker.name(),
            'price': round(random.uniform(50, 1000), 2),
            'countInStock': round(random.randrange(5, 50), 2),
            'description': self.faker.text(random.randrange(500, 2000)).replace('\n', ''),
            'rating': round(random.uniform(0,5), 2),

            'brand': random.choice(self.brands),
            'views': random.randrange(0, 100),
            'orderCount': random.randrange(0, 500), 

            'image': self.set_img(),
            'image2': self.set_img(),
            'image3': self.set_img(),
            'image4': self.set_img(),
            'image5': self.set_img(),
        }

		self.data_count += 1

		print(f'[{self.data_count}] {product["name"]}')

		self.products += f'    {product},\n'

	def manage_products(self):
		print(f'--> Creating {self.num_of_product} Products...')

		self.faker = Faker()

		for _ in range(self.num_of_product):
			self.create_product()

		self.products = f'const products = [\n{self.products}]\n\n module.exports = products'

		with open(f'{self.product_folder}/products.js', 'w') as file:
			file.write(self.products)
			file.close()

	def create(self):
		print('--> Starting...')

		self.delete_folder(self.product_folder)
		self.create_folder(self.product_img_folder)

		self.manage_products()


data_creator = DataCreator()
data_creator.create()