# Blueprint I/O

## Blueprint I/O moves blueprints around

* Centralized configuration management.
* Export and backup server configurations.
* Push and pull blueprints anywhere.
* Bootstrap servers painlessly.

Blueprint I/O pushes and pulls blueprints to and from a Blueprint I/O Server, making it easy to use blueprints anywhere. DevStructure provides a free Blueprint I/O Server at <https://devstructure.com>, which stores blueprints in Amazon S3. Alternatively, you can build your own backend server using the Blueprint I/O API.

## Usage

### Push a blueprint

    blueprint push my-first-blueprint
    
The blueprint and its files are stored remotely.  You get a secret URL for accessing it.
	
### Pull a blueprint

    blueprint pull https://devstructure.com/MY-SECRET-KEY/my-first-blueprint
    
The blueprint is stored locally and ready for use.

## Installation

Prerequisites:

* A Debian- or RPM-based Linux distribution
* Python >= 2.6
* [Blueprint](https://github.com/devstructure/blueprint)

### From source on Debian, Ubuntu, and Fedora

	git clone git://github.com/devstructure/blueprint.git
	cd blueprint && make && sudo make install
	git clone git://github.com/devstructure/blueprint-io.git
	cd blueprint-io && make && sudo make install

### From source on CentOS and RHEL

	rpm -Uvh http://download.fedora.redhat.com/pub/epel/5/i386/epel-release-5-4.noarch.rpm
	yum install python26
	git clone git://github.com/devstructure/blueprint.git
	cd blueprint && make && sudo make install PYTHON=/usr/bin/python26
	git clone git://github.com/devstructure/blueprint-io.git
	cd blueprint-io && make && sudo make install PYTHON=/usr/bin/python26

This installs Python 2.6 from EPEL side-by-side with Python 2.4 and so won't break yum.

### With a package manager

DevStructure maintains Debian packages and Python eggs for Blueprint I/O.  See [Installing with a package manager](https://github.com/devstructure/blueprint-io/wiki/Installing-with-a-package-manager) on the wiki.

## Documentation

Tutorials and API details will land in the [documentation](https://devstructure.com/docs/) soon.

## Manuals

* [`blueprint-push`(1)](http://devstructure.github.com/blueprint-io/blueprint-push.1.html)
* [`blueprint-pull`(1)](http://devstructure.github.com/blueprint-io/blueprint-pull.1.html)
* [`blueprint-io`(7)](http://devstructure.github.com/blueprint-io/blueprint-io.7.html)

## Contribute

Blueprint I/O is [BSD-licensed](https://github.com/devstructure/blueprint-io/blob/master/LICENSE).

* Source code: <https://github.com/devstructure/blueprint-io>
* Issue tracker: <https://github.com/devstructure/blueprint-io/issues>
* Documentation: <https://devstructure.com/docs/>
* Wiki: <https://github.com/devstructure/blueprint-io/wiki>
* Mailing list: <https://groups.google.com/forum/#!forum/blueprint-users>
* IRC: `#devstructure` on Freenode
