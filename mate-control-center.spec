Summary:	MATE Desktop control-center
Name:		mate-control-center
Version:	1.5.4
Release:	1
License:	LGPL v2+ and GPL v2+
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.5/%{name}-%{version}.tar.xz
# Source0-md5:	71545e5ffe56f45da2fe8f6cac6c8009
URL:		http://wiki.mate-desktop.org/mate-control-center
BuildRequires:	dbus-glib-devel
BuildRequires:	dconf-devel
BuildRequires:	desktop-file-utils
BuildRequires:	gsettings-desktop-schemas-devel
BuildRequires:	gtk+2-devel
BuildRequires:	icon-naming-utils
BuildRequires:	libcanberra-devel
BuildRequires:	libmatekbd-devel
BuildRequires:	libmatenotify-devel
BuildRequires:	librsvg-devel
BuildRequires:	libunique-devel
BuildRequires:	libxklavier-devel
BuildRequires:	mate-common
BuildRequires:	mate-desktop-devel
BuildRequires:	mate-doc-utils
BuildRequires:	mate-menus-devel
BuildRequires:	mate-settings-daemon-devel
BuildRequires:	mate-window-manager-devel
BuildRequires:	nss-devel
BuildRequires:	polkit-devel
BuildRequires:	rpmbuild(find_lang) >= 1.36
BuildRequires:	rpmbuild(macros) >= 1.596
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libICE-devel
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libXScrnSaver-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXxf86misc-devel
BuildRequires:	xorg-lib-libxkbfile-devel
BuildRequires:	xz
Requires:	%{name}-libs = %{version}-%{release}
Requires:	desktop-file-utils
Requires:	glib2 >= 1:2.26.0
Requires:	gsettings-desktop-schemas
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
Requires:	shared-mime-info
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MATE Desktop Control Center.

%package libs
Summary:	MATE Control Center libmate-window-settings library
Summary(pl.UTF-8):	Biblioteka Control Center libmate-window-settings
Group:		X11/Libraries
Conflicts:	mate-control-center < 1.5.3-2

%description libs
This package contains libmate-window-settings library.

%description libs -l pl.UTF-8
Pakiet ten zawiera bibliotekę libmate-window-settings.

%package devel
Summary:	Development files for mate-settings-daemon
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Development files for mate-control-center

%prep
%setup -q

%build
NOCONFIGURE=1 ./autogen.sh
%configure \
	--with-html-dir=%{_gtkdocdir} \
	--disable-static \
	--disable-schemas-compile \
	--disable-update-mimedb \
	--disable-scrollkeeper

%{__make} \
	V=1

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libmate-window-settings.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libslab.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/window-manager-settings/libmarco.la

# mate < 1.5 did not exist in pld, avoid dependency on mate-conf
%{__rm} $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/mate-control-center.convert

desktop-file-install \
	--remove-category="MATE" \
	--add-category="X-Mate" \
	--delete-original \
	--dir=$RPM_BUILD_ROOT%{_desktopdir} \
$RPM_BUILD_ROOT%{_desktopdir}/*.desktop

# delete mime cache
%{__rm} $RPM_BUILD_ROOT%{_desktopdir}/mimeinfo.cache

%find_lang %{name} --with-mate --with-omf --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database
%update_icon_cache hicolor
%update_mime_database
%glib_compile_schemas

%postun
%update_desktop_database_postun
%update_icon_cache hicolor
%update_mime_database
%glib_compile_schemas

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING README
%{_sysconfdir}/xdg/menus/matecc.menu
%attr(755,root,root) %{_bindir}/mate-*
%attr(755,root,root) %{_sbindir}/mate-display-properties-install-systemwide
%dir %{_libdir}/window-manager-settings
%attr(755,root,root) %{_libdir}/window-manager-settings/libmarco.so
%{_desktopdir}/*.desktop
%{_datadir}/desktop-directories/matecc.directory
%{_iconsdir}/hicolor/*/apps/*.*
%{_datadir}/glib-2.0/schemas/org.mate.*.xml
%{_datadir}/mate-control-center
%{_datadir}/mime/packages/mate-theme-package.xml
%{_datadir}/thumbnailers/mate-font-viewer.thumbnailer
%{_datadir}/polkit-1/actions/org.mate.randr.policy

# referred as builtins in capplets/common/mate-theme-info.c
# http://git.gnome.org/browse/gnome-control-center/tree/capplets/common/gnome-theme-info.c?id=GNOME_CONTROL_CENTER_2_32_1
%dir %{_datadir}/mate/cursor-fonts
# TODO: maybe .gzlike other fonts in %{_datadir}/fonts/misc/*.pcf.gz?
%{_datadir}/mate/cursor-fonts/*.pcf

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmate-window-settings.so.*.*.*
%ghost %{_libdir}/libmate-window-settings.so.1
%attr(755,root,root) %{_libdir}/libslab.so.*.*.*
%ghost %{_libdir}/libslab.so.0

%files devel
%defattr(644,root,root,755)
%{_includedir}/libslab
%{_includedir}/mate-window-settings-2.0
%{_libdir}/libmate-window-settings.so
%{_libdir}/libslab.so
%{_npkgconfigdir}/mate-default-applications.pc
%{_npkgconfigdir}/mate-keybindings.pc
%{_pkgconfigdir}/libslab.pc
%{_pkgconfigdir}/mate-window-settings-2.0.pc
