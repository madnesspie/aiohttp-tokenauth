import os

import setuptools

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

INSTALL_REQUIRES = [
    'aiohttp',
]

setuptools.setup(
    name='aiohttp-tokenauth',
    version='0.0.1',
    description='Simple way to add token auth level in your aiohttp app',
    platforms=['POSIX'],
    author='Alexander Polishchuk',
    author_email='apolishchuk52@gmail.com',
    url='https://github.com/madnesspie/aiohttp-tokenauth',
    packages=setuptools.find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    license='GNU General Public License v3 or later (GPLv3+)',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: AsyncIO',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Intended Audience :: Developers',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    long_description=README,
    long_description_content_type='text/markdown',
)
