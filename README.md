[![Tests](https://github.com/OpenDataGIS/ckanext-bne/workflows/Tests/badge.svg?branch=main)](https://github.com/OpenDataGIS/ckanext-bne/actions)

# ckanext-bne

Customization extension for the Open Data portal of the BNE 

### Features
* Dataset showcase on the home screen
* BNE api integration
* Stylized to be similar to the BNE style
  
![image](https://github.com/user-attachments/assets/6d67ef52-3d59-4e8b-9233-e65e59b582db)


## Requirements

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.6 and earlier | not tested    |
| 2.7             | not tested    |
| 2.8             | not tested    |
| 2.9             | not tested    |
| 2.10            | yes           |


## Installation

To install ckanext-bne:

1. Activate your CKAN virtual environment, for example:

     . /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv

    git clone https://github.com/OpenDataGIS/ckanext-bne.git
    cd ckanext-bne
    pip install -e .
	pip install -r requirements.txt

3. Add `bne` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

     sudo service apache2 reload
   

## Config settings

* bne_base_url: Bne URL
* bne_api_base_url: Bne API URL
* bne_api_tables: bne API table mapping, format  `{ <humanized_name> : <api_table>, ... }`
* bne_api_pill_style: bne API table mapping, format  `{ <humanized_name> : {'icon':'<font_awesome_icon>','color':'<color_hex (optional)>'} ... }`
* bne_api_entries: number of entries to be shown by default on the API

```python
# example config on ckanext-bne/ckanext/bne/config.py

bne_base_url = "https://www.bne.es/"
bne_api_base_url = "http://<url>/api/"
bne_api_tables = {'Geográfico': 'geo',
                'Persona': 'per',
                ...
                }
bne_api_pill_style = {'Geográfico': {'icon':'fas fa-atlas'},
                'Persona': {'icon':'fas fa-user'},
                ...
                }
bne_api_entries = 20
```


## Developer installation

To install ckanext-bne for development, activate your CKAN virtualenv and
do:

    git clone https://github.com/OpenDataGIS/ckanext-bne.git
    cd ckanext-bne
    python setup.py develop
    pip install -r dev-requirements.txt


## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini


## Releasing a new version of ckanext-bne

If ckanext-bne should be available on PyPI you can follow these steps to publish a new version:

1. Update the version number in the `setup.py` file. See [PEP 440](http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers) for how to choose version numbers.

2. Make sure you have the latest version of necessary packages:

    pip install --upgrade setuptools wheel twine

3. Create a source and binary distributions of the new version:

       python setup.py sdist bdist_wheel && twine check dist/*

   Fix any errors you get.

4. Upload the source distribution to PyPI:

       twine upload dist/*

5. Commit any outstanding changes:

       git commit -a
       git push

6. Tag the new release of the project on GitHub with the version number from
   the `setup.py` file. For example if the version number in `setup.py` is
   0.0.1 then do:

       git tag 0.0.1
       git push --tags

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html) \
includes code from https://tabulator.info/ - License: https://github.com/olifolkerd/tabulator?tab=MIT-1-ov-file

