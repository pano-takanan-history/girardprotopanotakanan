from setuptools import setup
import json


with open('metadata.json', encoding='utf-8') as fp:
    metadata = json.load(fp)


setup(
    name="lexibank_girardprotopanotakanan",
    description=metadata["title"],
    license=metadata.get("license", ""),
    url=metadata.get("url", ""),
    py_modules=["lexibank_girardprotopanotakanan"],
    include_package_data=True,
    zip_safe=False,
    entry_points={"lexibank.dataset": ["girardprotopanotakanan=lexibank_girardprotopanotakanan:Dataset"]},
    install_requires=["pylexibank>=3.0.0", "pyedictor"],
    extras_require={"test": ["pytest-cldf"]},
)