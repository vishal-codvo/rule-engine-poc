from setuptools import setup, find_packages

setup(
    name="sensor-rule-engine",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'nats-py',
        'asyncio',
        'business-rules',
        'psycopg2-binary',
        'sqlalchemy',
        'python-dotenv',
        'pytest',
        'pytest-asyncio',
        'pytest-cov'
    ],
) 