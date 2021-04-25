from setuptools import setup, find_packages

setup(
        name='Byte.py',
        version='0.4',
        description='A Python API Wrapper to interact with with the SocialMedia platform Byte.co',
        long_description="""
        # ByteAPI
        Byte.py is a python wrapper for the inofficial API that runs the SocialMedia platform Byte.co. This is pretty basic as of now, and will be updated in future releases. For more information about this package's capabilities please refer to the documentation.
        # Basic usage
        The following snippet is an example on how to create a new Byte.py client instance and fetch the username of the logged-in user.
        ```python
        from ByteAPI import ByteAPI

        byteClient = ByteAPI(<Your Token>)
        print(byteClient.username)
        ```
        """,
        long_description_content_type='text/markdown',
        url='https://rpwnage.github.io/ByteAPI/',
        author='rpwnage',
        author_email='rpwnage@protonmail.com',
        license='MIT',
        packages=find_packages(),
        install_requires=["requests"],
        keywords=['api', 'byte.co', 'byte'],
        zip_safe=False
    )
