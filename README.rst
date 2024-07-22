=============
ckanext-bibliotecanacional
=============

.. CKAN customization for the Ibiza Island Council


------------
Installation
------------

To install ckanext-bibliotecanacional:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-bibliotecanacional Python package into your virtual environment::

     cd /usr/lib/ckan/default/src
     git clone https://github.com/localidata/ckanext-bibliotecanacional
     cd ckanext-bibliotecanacional
     python setup.py develop

3. Add ``bibliotecanacional`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/ckan.ini``).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload


