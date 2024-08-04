from setuptools import setup, find_packages

setup(
    name='python_logging',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'colorama',
    ],
    include_package_data=True,
    package_data={
        '': ['log_colors.json'],
    },
    description='A Python module for advanced logging with color themes',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Mythical-Github/python_logging',
    author='Mythical',
    author_email='mythicaldata.com',
    license='GPL3',
)
