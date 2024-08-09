from setuptools import setup, find_packages

setup(
    name='log_py',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'colorama'
    ],
    include_package_data=True,
    package_data={
        '': ['log_colors.json.example'],
    },
    description='',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Mythical-Github/log_py',
    author='Mythical',
    author_email='mythicaldata.com',
    license='GPL-3.0',
)
