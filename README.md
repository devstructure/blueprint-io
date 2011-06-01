# Blueprint I/O

`blueprint-io` is a tool for pushing and pulling blueprints to or from a remote server. A local blueprint is pushed to a blueprint-io server. A remote blueprint is pulled from a blueprint-io server. Pushes and pulls account for both the JSON and tarball portions of a blueprint. 

DevStructure offers a free blueprint-io server at https://devstructure.com, the data is stored on Amazon S3. The DevStrucure blueprint-io server is specified as a default or you can set your own in /etc/blueprint-io.cfg or ~/.blueprint-io.cfg. 

## Try it now!

	git clone git://github.com/devstructure/blueprint-io.git
	cd blueprint-io
	make && sudo make install

	blueprint push blueprint_name
	blueprint pull https://devstructure.com/MY_LONG_SECRET_KEY/blueprint_name


## Contribute

`blueprint-io` is BSD-licensed.  We love bug reports and pull requests!

* [Source code](https://github.com/devstructure/blueprint-io)
* [Issue tracker](https://github.com/devstructure/blueprint-io/issues)
* [Documentation](http://devstructure.github.com/blueprint/)
* [Discuss](https://groups.google.com/forum/#!forum/blueprint-users) or `#devstructure` on Freenode

## Protocol
