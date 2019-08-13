from distutils.core import setup
from setuptools import find_packages
from req import reqs

setup(
    name='algonaut',
    python_requires='>=3',
    version='0.0.2',
    author='Andreas Dewes',
    author_email='andreas.dewes@algoneer.org',
    license='GNU Affero General Public License - Version 3 (AGPL-3)',
    url='https://github.com/algoneer/algonaut',
    packages=find_packages(),
    package_data={'': ['*.yml', '*.sql']},
    include_package_data=True,
    install_requires=reqs,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'algonaut = algonaut.cli.main:main'
        ]
    },
    description='The API toolkit for Algoneer.',
    long_description="""The API toolkit for Algoneer.
"""
)
