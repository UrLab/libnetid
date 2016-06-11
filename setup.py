from setuptools import setup, find_packages

setup(
    name='libnetid',
    version='0.1.dev',
    description='Interact with the ULB SSO in python',
    url='https://github.com/C4ptainCrunch/libnetid',
    author='Nikita Marchant',
    author_email='nikita.marchant@ulb.ac.be',
    license='BSD',
    packages=find_packages(exclude="[examples]"),
    zip_safe=False,
    install_requires=[
        'requests',
        'furl',
    ],
)
