from setuptools import setup, find_packages

setup(
    name='django-facebook-connect',
    version=__import__('facebook_connect').__version__,
    license="MIT",
    install_requires = [
        'Django',
    ],
    description='Add facebook connect authentication to your Django website.',
    long_description=open('README.md').read(),
    author='Noam Sutskever',
    author_email='noamsu@gmail.com',
    url='http://github.com/noamsu/django-facebook-connect',
    download_url='http://github.com/noamsu/django-facebook-connect/downloads',
    include_package_data=True,
    packages=['facebook_connect'],
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)