from pip.download import PipSession
from pip.req import parse_requirements
from os.path import join, dirname
from setuptools import setup, find_packages


def requires():
    return [str(item.req)
            for item in parse_requirements('requirements.txt', session=PipSession())
            if item.req]


def links():
    return [str(item.link)
            for item in parse_requirements('requirements.txt', session=PipSession())
            if item.link]


def read(fname):
    return open(join(dirname(__file__), fname)).read()


setup(
    name='eye-keyboard',
    version='0.0.1',
    author='Emanuel Vianna',
    author_email='emanuelvianna@gmail.com',
    description="Extending webcam-eyetracker for use a keyboard with pupils",
    license='GPL',
    keywords="webcam avc eye pupils keyboard tracker",
    url="https://github.com/emanuelvianna/eye-keyboard",
    packages=find_packages(),
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Topic :: Adaptive Technologies"
    ],
    install_requires=requires(),
    dependency_links=links(),
    zip_safe=False,
    platforms='any',
    entry_points={'console_scripts': ['eye-keyboard=eye_keyboard.app:main']},
    package_data={'eye_keyboard': ['resources/*.wav', 'resources/*.png', 'resources/*.ttf']},
)

