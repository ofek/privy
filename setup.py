from setuptools import find_packages, setup

setup(
    name='privy',
    version='4.0.0',
    description='Password-protected secrets made easy.',
    long_description=open('README.rst', 'r').read(),
    author='Ofek Lev',
    author_email='ofekmeister@gmail.com',
    url='https://github.com/ofek/privy',
    license='MIT',

    keywords=(
        'passwords',
        'secrets',
        'encryption',
        'keys',
        'aes',
        'hmac',
    ),

    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ),

    install_requires=['cryptography', 'argon2_cffi'],
    tests_require=['pytest'],

    packages=find_packages(),
)
