from setuptools import setup

setup(
    name='rich_table',
    version='0.1.1',
    description='A login part that based on streamlit_authenticator',
    url='https://ghe.rakuten-it.com/zhichao-liu/login_helper',
    author='ZhiChao Liu',
    author_email='zhichao.liu@rakuten.com',
    packages=['rich_table'],
    install_requires=['streamlit-aggrid==1.0.4.post3'],

    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.10',
    ],
)
