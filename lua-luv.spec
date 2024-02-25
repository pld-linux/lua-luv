%bcond_without	lua51		# lua51 package
%bcond_without	luajit		# luajit package

%ifnarch %{ix86} %{x8664} %{arm} aarch64 mips mips64 mipsel ppc
%undefine	with_luajit
%endif

%define		real_version	1.48.0
%define		extra_version	0

%define		luajit_abi	2.1

Summary:	Bare libuv bindings for lua
Name:		lua-luv
Version:	%{real_version}.%{extra_version}
Release:	1
License:	Apache v2.0
Group:		Libraries
Source0:	https://github.com/luvit/luv/releases/download/v%{real_version}-%{extra_version}/luv-v%{real_version}-%{extra_version}.tar.gz
# Source0-md5:	ba3b191ca7e953970d43be2e7c50c870
URL:		https://github.com/luvit/luv
BuildRequires:	cmake >= 3.5
BuildRequires:	libuv-devel
BuildRequires:	lua-devel >= 5.4
BuildRequires:	rpmbuild(macros) >= 1.605
%if %{with lua51}
BuildRequires:	lua51-devel
%endif
%if %{with luajit}
BuildRequires:	luajit-devel
%endif
Requires:	lua54-libs
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
Group:		Development/Libraries
Requires:	lua-luv = %{version}-%{release}
Requires:	lua54-devel

%description devel
Files required for lua-luv development

%package -n lua51-luv
Summary:	Bare libuv bindings for lua
Requires:	lua51-libs

%description -n lua51-luv
This library makes libuv available to lua scripts. It was made for the
luvit project but should usable from nearly any lua project.

The library can be used by multiple threads at once. Each thread is
assumed to load the library from a different lua_State. Luv will
create a unique uv_loop_t for each state. You can't share uv handles
between states/loops.

The best docs currently are the libuv docs themselves. Hopefully soon
we'll have a copy locally tailored for lua.

Package for Lua 5.1.

%package -n lua51-luv-devel
Summary:	Development files for lua51-luv
Group:		Development/Libraries
Requires:	lua51-luv = %{version}-%{release}
Requires:	lua51-devel

%description -n lua51-luv-devel
Files required for lua51-luv development

%package -n luajit-luv
Summary:	Bare libuv bindings for lua
Requires:	luajit-libs

%description -n luajit-luv
This library makes libuv available to lua scripts. It was made for the
luvit project but should usable from nearly any lua project.

The library can be used by multiple threads at once. Each thread is
assumed to load the library from a different lua_State. Luv will
create a unique uv_loop_t for each state. You can't share uv handles
between states/loops.

The best docs currently are the libuv docs themselves. Hopefully soon
we'll have a copy locally tailored for lua.

Package for LuaJIT.

%package -n luajit-luv-devel
Summary:	Development files for luajit-luv
Group:		Development/Libraries
Requires:	luajit-luv = %{version}-%{release}
Requires:	luajit-devel

%description -n luajit-luv-devel
Files required for luajit-luv development

%prep
%setup -q -n luv-v%{real_version}-%{extra_version}

# Remove bundled dependencies
rm -r deps/{lua.cmake,luajit.cmake,libuv}
# Remove network sensitive tests gh#luvit/luv#340
rm -f tests/test-dns.lua

%build
%cmake -B build \
	-DWITH_SHARED_LIBUV=ON \
	-DBUILD_MODULE=ON \
	-DBUILD_SHARED_LIBS=ON \
	-DWITH_LUA_ENGINE=Lua \
	-DLUA_BUILD_TYPE=System \
	-DINSTALL_LIB_DIR=%{_libdir} \
	-DLUA_INCLUDE_DIR=%{_includedir}/lua5.4

%{__make} -C build

%if %{with tests}
ln -sfn build/luv.so luv.so
lua tests/run.lua
rm luv.so
%endif

%if %{with lua51}
%cmake -B build-lua51 \
	-DWITH_SHARED_LIBUV=ON \
	-DBUILD_MODULE=ON \
	-DBUILD_SHARED_LIBS=ON \
	-DWITH_LUA_ENGINE=Lua \
	-DLUA_BUILD_TYPE=System \
	-DINSTALL_LIB_DIR=%{_libdir} \
	-DLUA_INCLUDE_DIR=%{_includedir}/lua5.1

%{__make} -C build-lua51
%endif

%if %{with luajit}
%cmake -B build-luajit \
	-DWITH_SHARED_LIBUV=ON \
	-DBUILD_MODULE=ON \
	-DBUILD_SHARED_LIBS=ON \
	-DWITH_LUA_ENGINE=LuaJIT \
	-DLUA_BUILD_TYPE=System \
	-DINSTALL_LIB_DIR=%{_libdir} \
	-DLUA_INCLUDE_DIR=%{_includedir}/luajit-%{luajit_abi}

%{__make} -C build-luajit
%endif

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/lua/5.4
install -p build/luv.so $RPM_BUILD_ROOT%{_libdir}/lua/5.4/luv.so

install -d $RPM_BUILD_ROOT%{_includedir}/lua5.4/luv
for f in lhandle.h lreq.h luv.h util.h; do
	install -m 0644 -p src/$f $RPM_BUILD_ROOT%{_includedir}/lua5.4/luv/$f
done

%if %{with lua51}
install -d $RPM_BUILD_ROOT%{_libdir}/lua/5.1
install -p build-lua51/luv.so $RPM_BUILD_ROOT%{_libdir}/lua/5.1/luv.so

install -d $RPM_BUILD_ROOT%{_includedir}/lua5.1/luv
for f in lhandle.h lreq.h luv.h util.h; do
	install -m 0644 -p src/$f $RPM_BUILD_ROOT%{_includedir}/lua5.1/luv/$f
done
%endif

%if %{with luajit}
install -d $RPM_BUILD_ROOT%{_libdir}/luajit/%{luajit_abi}
install -p build-luajit/luv.so $RPM_BUILD_ROOT%{_libdir}/luajit/%{luajit_abi}/luv.so

install -d $RPM_BUILD_ROOT%{_includedir}/luajit-%{luajit_abi}/luv
for f in lhandle.h lreq.h luv.h util.h; do
	install -m 0644 -p src/$f $RPM_BUILD_ROOT%{_includedir}/luajit-%{luajit_abi}/luv/$f
done
%endif

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

%if %{with lua51}
%files -n lua51-luv
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/lua/5.1/luv.so

%files -n lua51-luv-devel
%defattr(644,root,root,755)
%dir %{_includedir}/lua5.1/luv
%{_includedir}/lua5.1/luv/lhandle.h
%{_includedir}/lua5.1/luv/lreq.h
%{_includedir}/lua5.1/luv/luv.h
%{_includedir}/lua5.1/luv/util.h
%endif

%if %{with luajit}
%files -n luajit-luv
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/luajit/%{luajit_abi}/luv.so

%files -n luajit-luv-devel
%defattr(644,root,root,755)
%dir %{_includedir}/luajit-%{luajit_abi}/luv
%{_includedir}/luajit-%{luajit_abi}/luv/lhandle.h
%{_includedir}/luajit-%{luajit_abi}/luv/lreq.h
%{_includedir}/luajit-%{luajit_abi}/luv/luv.h
%{_includedir}/luajit-%{luajit_abi}/luv/util.h
%endif
