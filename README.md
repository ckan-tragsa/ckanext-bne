[![Tests](https://github.com/OpenDataGIS/ckanext-bne/workflows/Tests/badge.svg?branch=main)](https://github.com/OpenDataGIS/ckanext-bne/actions)

# ckanext-bne

**TODO:** Put a description of your extension here:  What does it do? What features does it have? Consider including some screenshots or embedding a video!


## Requirements

**TODO:** For example, you might want to mention here which versions of CKAN this
extension works with.

If your extension works across different versions you can add the following table:

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.6 and earlier | not tested    |
| 2.7             | not tested    |
| 2.8             | not tested    |
| 2.9             | yes           |
| 2.10            | yes           |

Suggested values:

* "yes"
* "not tested" - I can't think of a reason why it wouldn't work
* "not yet" - there is an intention to get it working
* "no"


## Installation

**TODO:** Add any additional install steps to the list below.
   For example installing any non-Python dependencies or adding any required
   config settings.

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

None at present

**TODO:** Document any optional config settings here. For example:

	# The minimum number of hours to wait before re-checking a resource
	# (optional, default: 24).
	ckanext.bne.some_setting = some_default_value


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

## Development
### Update Internationalization (i18n) Files
To compile a `.po` file to a `.mo` file in the terminal, you can use the `msgfmt` tool, which is part of the `gettext` package. Here are the steps to do it:

### Steps to Compile `.po` File to `.mo` File.

1. **Install `gettext` (if not already installed)**:
   - On most Linux distributions, you can install `gettext` using your system's package manager. For example, in Debian/Ubuntu:

   ```sh
   sudo apt-get install gettext
   ```

   In Fedora:

   ````sh
   sudo dnf install gettext
   ```

2. **Compile the `.po` file to `.mo`**:
   - Use the `msgfmt` command to compile the `.po` file to `.mo`. **Make sure you are in the directory where your `.po` file is located or provide the full path to the file.**

   ```sh
   msgfmt -o ckanext-bne.mo ckanext-bne.po
   ```

   - This command will generate a `ckanext-bne.mo` file in the same directory as the `.po` file.

### Complete Example

Let's assume your `.po` file is located in the `i18n/en/LC_MESSAGES/` directory inside your project. Here are the complete commands:

1. 1. **Navigate to the Project Directory**:

   ```sh
   cd /path/to/your/project
   ```

2. **Navigate to the Directory Containing the `.po`** File:

   ````sh
   cd i18n/en/LC_MESSAGES/
   ```

3. **Compile the `.po` file to `.mo`**:

   ````sh
   msgfmt -o ckanext-bne.mo ckanext-bne.po
   ```

### Verification

1. **Verify that the `.mo` file has been generated in the browser.

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
