from setuptools import find_packages, setup


setup(
    # Package information:
    name='yatron',
    version='1.0.0',
    license='GNU GPL',
    url='http://github.com/aatiis/python-yatron',
    description='Tron board and utilities.',
    long_description='%s\n\n%s'%(
        open('README.txt').read(),
        open('CHANGES.txt').read(),
    ),
    # Author information:
    author='Attila Olah',
    author_email='attilaolah@gmail.com',
    # Package settings:
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    zip_safe=True,
    # Classifiers:
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Framework :: Buildout',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Education',
        'Topic :: Games/Entertainment',
        'Topic :: Games/Entertainment :: Simulation',
    ),
)
