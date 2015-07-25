from __future__ import with_statement
import os

from setuptools import setup, find_packages

from django_type_of_works import __version__ as version#fix


install_requires = []

try:
    setup(
        name="django-type-of-works",
        version=version,
        author="Victor De la Luz",
        author_email="itztli@gmail.com",
        description="Type of works.",
        long_description=open("README.rst").read(),
        license="BSD",
        #url="http://mezzanine.jupo.org/",
        zip_safe=False,
        include_package_data=True,
        packages=find_packages(),
        install_requires=install_requires,
        entry_points="""
            [console_scripts]
        """,
        classifiers=[
            "Development Status :: 4 - Beta",
            "Environment :: Web Environment",
            "Framework :: Django",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: BSD License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Topic :: Internet :: WWW/HTTP",
            "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
            "Topic :: Internet :: WWW/HTTP :: WSGI",
            "Topic :: Software Development :: Libraries :: "
                                                "Application Frameworks",
            "Topic :: Software Development :: Libraries :: Python Modules",
        ],)
except:
    pass
