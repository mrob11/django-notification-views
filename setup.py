from distutils.core import setup

setup(
    name='django-notification-views',
    version='0.1.0',
    author='Mike Robinson',
    author_email='mike.robinson.81@gmail.com',
    packages=['notification',],
    url='http://github.com/mike360/django-notification-views/',
    license='BSD',
    description='Generic class-based views and mix-ins incorporating the \
        Django messaging framework for automatic, extensible notification.',
    long_description=open('README.md').read(),
    install_requires=[
        "Django >= 1.3",
    ],
)