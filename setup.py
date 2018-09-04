import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

CLASSIFIERS = [
    'Environment :: Web Environment',
    'Framework :: Django',
    'Framework :: Django :: 2.1',
    'Framework :: Wagtail',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
]


install_requires = [
    'django-import-export',
]

setup(
    name='wagtail-exportcsv',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',  # example license
    description='A simple Django wagtail app to download form submissions as CSV.',
    long_description=README,
    url='https://github.com/7aleb/wagtail-exportcsv',
    author='Mohammad Taleb',
    author_email='shimultaleb@gamil.com',
    install_requires=install_requires,
    classifiers=CLASSIFIERS,
)