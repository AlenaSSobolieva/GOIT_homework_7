from setuptools import setup, find_namespace_packages

setup(name='clean_folder',
      version='1.0',
      description='Clean and manage files',
      author='Olena Sobolieva',
      author_email='soboleva13as@gmail.com',
      licenses='MIT',
      packages=find_namespace_packages(),
      entry_points={'console_scripts': ['clean_folder=clean_folder.clean:start']}
      )