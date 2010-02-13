from setuptools import find_packages, setup


setup(
    # Package information
    name='yatron',
    version='1.0.0',
    license='GNU GPL',
    url='http://github.com/aatiis/python-yatron',
    description='Tron board and utilities.',
    # Author information
    author='Attila Olah',
    author_email='attilaolah@gmail.com',
    # Package settings
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    zip_safe=True,
)
