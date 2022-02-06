from faker import Faker
from PIL import Image
import os
import glob
import random
import shutil


class PopulateProduct:
    def __init__(self):
        self.cur_dir = os.getcwd().replace('\\', '/')
        self.main_folder = 'products/'
        self.image_folder = self.main_folder + 'images/'
        self.brands = ['Apple', 'Tesla', 'Microsoft',
                       'Nike', 'Himel Bikon', 'Facebook']
        self.data_count = 0
        self.faker = Faker()

    def folder_creator(self, folder):
        if not os.path.exists(folder):
            os.makedirs(folder)
            print('Folder created!')

    def set_img(self):
        path = os.getcwd().replace('\\', '/') + '/images/*.jpg'
        images = list(map(lambda x: x.replace('\\', '/'), glob.glob(path)))

        image = random.choice(images)
        image_name = image.split('/')[-1]

        target = os.getcwd().replace('\\', '/') + '/products/images/' + image_name
        shutil.copyfile(image, target)

        self.resize(target, 500, 300)

        return image_name

    def resize(self, image_path, width, height):
        img = Image.open(image_path)
        size = (width, height)
        img = img.resize(size)
        img.save(image_path)

    def create_product(self):
        product = {
            'name': self.faker.name(),
            'price': round(random.uniform(50, 1000), 2),
            'countInStock': round(random.randrange(5, 50), 2),
            'details': self.faker.text(random.randrange(500, 2000)).replace('\n', ''),

            'brand': random.choice(self.brands),
            'views': random.randrange(0, 100),

            'image': self.set_img(),
            'image2': self.set_img(),
            'image3': self.set_img(),
            'image4': self.set_img(),
            'image5': self.set_img(),

        }

        self.data_count += 1
        print(f'[{self.data_count}] {product["name"]}')
        return f'    {product},\n'

    def demo_products(self, loop_num):
        print(f'[+] Creating {loop_num} Products...')

        products = ''
        faker = Faker()

        for _ in range(loop_num):
            products += (self.create_product())

        return f'const products = [\n{products}]'

    def delete_all_files(self):
        path = self.cur_dir + '/products/images'

        if os.path.exists(path):
            print(f'[+] Deleting Previous Images...')

            for file in os.listdir(path):
                os.remove(path + '/' + file)

    def start(self):
        self.delete_all_files()

        self.folder_creator(self.main_folder)
        self.folder_creator(self.image_folder)

        products = str(self.demo_products(10))

        with open(f'{self.main_folder}/products.js', 'w') as file:
            file.write(products)
            file.close()


populate_product = PopulateProduct()
populate_product.start()
