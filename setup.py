from setuptools import setup, find_packages

def parse_requirements():
    """Parse the dependencies from the requirements.txt file."""
    with open('requirements.txt') as f:
        return f.read().splitlines()

setup(
    name='PredigtenUploader',
    version='0.3.1',
    description='Eine Anwendung zum Hochladen von Predigten von Youtube auf einen externen Server',
    author='Johannes S. Post',

    # Specify the packages in 'src' and include 'main.py' in the root
    packages=find_packages(where='src'),  # Finds packages in src/
    package_dir={'': 'src'},  # Maps 'src' as the root for your Python modules
    
    # Include non-code files (such as files in 'file/' and 'stored/')
    package_data={
        '': ['file/*', 'stored/*'],  # Include everything in 'file/' and 'stored/'
    },
    
    # Read dependencies from the requirements.txt file
    install_requires=parse_requirements(),
    
    # Define entry points for console commands
    entry_points={
        'console_scripts': [
            'predigt_uploader=main:main',  # Entry point to the main function in main.py
        ],
    },

    # Include other metadata
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    
    python_requires='>=3.6',
)
