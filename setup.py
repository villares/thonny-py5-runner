import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='thonny-py5-runner',
    version='0.0.3',
    author='Alexandre Villares',
    description='A plugin to run your Python code with a py5 helper in Thonny IDE.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/villares/thonny-py5-runner',
    packages=['thonnycontrib.thonny_py5_runner'],
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=['thonny >= 3.0.0', 'py5'],
    python_requires='>=3.8',
)
