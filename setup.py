from setuptools import setup, find_packages

setup(
    name='invoices',
    version='0.1.0',
    description='Generate DOCX Invoice based on Toggl report and Google Docs template.',
    author='shapiy',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'invoices = invoices:main'
        ]
    }
)
