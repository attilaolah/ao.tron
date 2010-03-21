import os

from setuptools import find_packages, setup


setup(
    # Package information:
    name='ao.tron',
    version='1.0.0',
    license='GNU GPL',
    url='http://github.com/aatiis/ao.tron',
    description='Tron board and utilities.',
    long_description=\
        open('README.txt').read() + \
        open(os.path.join('src', 'ao', 'tron', 'board.txt')).read() + \
        open(os.path.join('src', 'ao', 'tron', 'input.txt')).read() + \
        open('CHANGES.txt').read(),
    # Author information:
    author='Attila Olah',
    author_email='attilaolah@gmail.com',
    # Package settings:
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    zip_safe=True,
    tests_require=(
        'zope.testing',
    ),
    extras_require={
        'test': (
            'zope.testing'
        ),
        'docs': (
            'Sphinx',
            'z3c.recipe.sphinxdoc',
        ),
    },
    # Classifiers:
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Framework :: Buildout',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Education',
        'Topic :: Games/Entertainment',
        'Topic :: Games/Entertainment :: Simulation',
    ],
)
