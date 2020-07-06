import setuptools

with open("README.md") as readme_file:
    long_description = readme_file.read()

with open("requirements.txt") as requirements_file:
    requirements = requirements_file.readlines()

setuptools.setup(
    name="yt-sub-importer",
    version="0.0.1",
    author="dorky dev",
    author_email="dorkdev99@gmail.com",
    description="An importer tool using Selenium for YouTube subscriptions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/0x3d904f/ChatSystem",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'yt-sub-importer = yt-sub-importer.main:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Topic :: Internet :: WWW/HTTP"
    ],
    install_requires=requirements,
    zip_safe=False,
    python_requires='>=3.8'
)
