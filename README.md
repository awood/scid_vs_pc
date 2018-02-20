This repository is used to build [Scid vs
PC](https://sourceforge.net/projects/scidvspc/) in a [Fedora
COPR](https://copr.fedorainfracloud.org/coprs/awood/scid_vs_pc/) project.

To build:

* Download the source tarball from the Scid vs PC homepage
* Install rpkg
* Run `rpkg srpm`
* Or alternatively `rpmbuild --define "_sourcedir $(pwd)" --define "_rpmdir
  $(pwd)" --define "_buildir $(pwd)" --define "_srcrpmdir $(pwd)" --define
  "_speccdir $(pwd)" -bs scid_vs_pc.spec`
