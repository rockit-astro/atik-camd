RPMBUILD = rpmbuild --define "_topdir %(pwd)/build" \
        --define "_builddir %{_topdir}" \
        --define "_rpmdir %{_topdir}" \
        --define "_srcrpmdir %{_topdir}" \
        --define "_sourcedir %(pwd)"

GIT_VERSION = $(shell git name-rev --name-only --tags --no-undefined HEAD 2>/dev/null || echo git-`git rev-parse --short HEAD`)
SERVER_VERSION=$(shell awk '/Version:/ { print $$2; }' qhy-camera-server.spec)

all:
	mkdir -p build
	${RPMBUILD} -ba observatory-atik-camera-client.spec
	${RPMBUILD} -ba python3-warwick-observatory-camera-atik.spec
	${RPMBUILD} -ba superwasp-atik-camera-data.spec
	mv build/noarch/*.rpm .
	rm -rf build
