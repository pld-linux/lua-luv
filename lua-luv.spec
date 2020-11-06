%global real_version 1.36.0
%global extra_version 0
Summary:	Bare libuv bindings for lua
Name:		lua-luv
Version:	%{real_version}.%{extra_version}
Release:	1
License:	Apache v2.0
BuildRequires:	cmake
BuildRequires:	libuv-devel
BuildRequires:	lua-devel >= 5.4
Source0:	https://github.com/luvit/luv/archive/%{real_version}-%{extra_version}/luv-%{version}.tar.gz
# Source0-md5:	5b9efde8652056faeb5ffc8f62f2b595
Patch0:		luv-1.36.0-lua-5.4.patch
URL:		https://github.com/luvit/luv
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library makes libuv available to lua scripts. It was made for the
luvit project but should usable from nearly any lua project.

The library can be used by multiple threads at once. Each thread is
assumed to load the library from a different lua_State. Luv will
create a unique uv_loop_t for each state. You can't share uv handles
between states/loops.

The best docs currently are the libuv docs themselves. Hopefully soon
we'll have a copy locally tailored for lua.

%package devel
Summary:	Development files for lua-luv
Requires:	lua-luv = %{version}-%{release}

%description devel
Files required for lua-luv development

%prep
%autosetup -p1 -n luv-%{real_version}-%{extra_version}

# Remove bundled dependencies
rm -r deps
# Remove network sensitive tests gh#luvit/luv#340
rm -f tests/test-dns.lua

%build
install -d build
cd build
%cmake \
	-DWITH_SHARED_LIBUV=ON \
	-DBUILD_MODULE=ON \
	-DBUILD_SHARED_LIBS=ON \
	-DWITH_LUA_ENGINE=Lua \
	-DLUA_BUILD_TYPE=System \
	-DINSTALL_LIB_DIR=%{_libdir} \
	-DLUA_INCLUDE_DIR=%{_includedir}/lua5.4 \
	..
cd ..

%{__make} -C build

%if %{with tests}
ln -sfn build/luv.so luv.so
lua tests/run.lua
rm luv.so
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/lua/5.4
install -p build/luv.so $RPM_BUILD_ROOT%{_libdir}/lua/5.4/luv.so

install -d $RPM_BUILD_ROOT%{_includedir}/lua5.4/luv
for f in lhandle.h lreq.h luv.h util.h; do
	install -m 0644 -p src/$f $RPM_BUILD_ROOT%{_includedir}/lua5.4/luv/$f
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/lua/5.4/luv.so

%files devel
%defattr(644,root,root,755)
%dir %{_includedir}/lua5.4/luv
%{_includedir}/lua5.4/luv/lhandle.h
%{_includedir}/lua5.4/luv/lreq.h
%{_includedir}/lua5.4/luv/luv.h
%{_includedir}/lua5.4/luv/util.h
