from setuptools import setup
import os

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django_ymap',
    version='2.1',
    packages=['django_ymap'],
    include_package_data=True,
    url='https://github.com/xacce/django-simple-yandex-map-v2/',
    license='MIT License',
    author='Xacce',
    author_email='mmodbrreceiver@gmail.com',
    description='Yandex maps admin intergration',
    long_description=README,
    install_requires=[]
)
