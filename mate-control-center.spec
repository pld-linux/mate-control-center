#
# Conditional build:
%bcond_without	appindicator	# application indicators support (in mate-typing-monitor)

Summary:	MATE Desktop control-center
Summary(pl.UTF-8):	Centrum sterowania środowiska MATE Desktop
Name:		mate-control-center
Version:	1.24.1
Release:	1
License:	LGPL v2+ (libmate-slab), GPL v2+ (the rest)
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.24/%{name}-%{version}.tar.xz
# Source0-md5:	bc900766bc520b5da46f1f56e083f207
URL:		http://wiki.mate-desktop.org/mate-control-center
BuildRequires:	accountsservice-devel >= 0.6.21
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake >= 1:1.9
BuildRequires:	dbus-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	dconf-devel >= 0.13.4
BuildRequires:	desktop-file-utils
BuildRequires:	docbook-dtd412-xml
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel >= 2
BuildRequires:	gettext-tools >= 0.19.8
BuildRequires:	glib2-devel >= 1:2.50.0
BuildRequires:	gtk+3-devel >= 3.22
%if %{with appindicator}
BuildRequires:	libappindicator-gtk3-devel >= 0.0.13
%endif
BuildRequires:	libcanberra-gtk3-devel
BuildRequires:	libmatekbd-devel >= 1.17.0
BuildRequires:	librsvg-devel >= 2.0
BuildRequires:	libtool >= 1:1.4.3
BuildRequires:	libxklavier-devel >= 5.2
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	marco-devel >= 1.17.0
BuildRequires:	mate-common
BuildRequires:	mate-desktop-devel >= 1.23.2
BuildRequires:	mate-menus-devel >= 1.21.0
BuildRequires:	mate-settings-daemon-devel >= 1.23.1
BuildRequires:	pango-devel
BuildRequires:	polkit-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(find_lang) >= 1.36
BuildRequires:	rpmbuild(macros) >= 1.596
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libICE-devel
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXScrnSaver-devel
BuildRequires:	xorg-lib-libXcursor-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXft-devel
BuildRequires:	xorg-lib-libXi-devel >= 1.5
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires:	%{name}-libs = %{version}-%{release}
Requires:	accountsservice-libs >= 0.6.21
Requires:	dconf >= 0.13.4
Requires:	desktop-file-utils
Requires:	gsettings-desktop-schemas
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
%if %{with appindicator}
Requires:	libappindicator-gtk3 >= 0.0.13
%endif
Requires:	libmatekbd >= 1.17.0
Requires:	libxklavier >= 5.2
Requires:	marco-libs >= 1.17.0
Requires:	mate-settings-daemon >= 1.23.1
Requires:	shared-mime-info
Conflicts:	libfm < 0.1.17-2
Conflicts:	lxappearance < 0.5.2-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MATE Desktop Control Center. The control center is MATE's main
interface for configuration of various aspects of your desktop.

%description -l pl.UTF-8
Centrum sterowania środowiska MATE Desktop. Jest to główny interfejs
do konfigurowania różnych aspektów pulpitu.

%package libs
Summary:	MATE Control Center libmate-window-settings library
Summary(pl.UTF-8):	Biblioteka libmate-window-settings centrum sterowania MATE
Group:		X11/Libraries
Requires:	glib2 >= 1:2.50.0
Requires:	gtk+3 >= 3.22
Requires:	mate-desktop-libs >= 1.23.2
Requires:	mate-menus-libs >= 1.21.0
Requires:	xorg-lib-libXi >= 1.5
Conflicts:	mate-control-center < 1.5.3-2

%description libs
This package contains libmate-window-settings library.

%description libs -l pl.UTF-8
Pakiet ten zawiera bibliotekę libmate-window-settings.

%package devel
Summary:	Development files for libmate-window-settings library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki libmate-window-settings
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.50.0
Requires:	gtk+3-devel >= 3.22
Requires:	mate-desktop-devel >= 1.23.2
Requires:	mate-menus-devel >= 1.21.0

%description devel
Development files for libmate-window-settings library.

%description devel -l pl.UTF-8
Pliki programistyczne biblioteki libmate-window-settings.

%prep
%setup -q

%build
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	%{!?with_appindicator:--disable-appindicator} \
	--disable-schemas-compile \
	--disable-silent-rules \
	--disable-static \
	--disable-update-mimedb

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/window-manager-settings/libmarco.la

# not supported by glibc
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{es_ES,frp,ie,jv,ku_IQ,pms}
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/help/{frp,ie,ku_IQ}

desktop-file-install \
	--remove-category="MATE" \
	--add-category="X-Mate" \
	--delete-original \
	--dir=$RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT%{_desktopdir}/*.desktop

# delete mime cache
%{__rm} $RPM_BUILD_ROOT%{_desktopdir}/mimeinfo.cache

%find_lang %{name} --with-mate

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
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/mate-about-me
%attr(755,root,root) %{_bindir}/mate-appearance-properties
%attr(755,root,root) %{_bindir}/mate-at-properties
%attr(755,root,root) %{_bindir}/mate-control-center
%attr(755,root,root) %{_bindir}/mate-default-applications-properties
%attr(755,root,root) %{_bindir}/mate-display-properties
%attr(755,root,root) %{_bindir}/mate-font-viewer
%attr(755,root,root) %{_bindir}/mate-keybinding-properties
%attr(755,root,root) %{_bindir}/mate-keyboard-properties
%attr(755,root,root) %{_bindir}/mate-mouse-properties
%attr(755,root,root) %{_bindir}/mate-network-properties
%attr(755,root,root) %{_bindir}/mate-thumbnail-font
%attr(755,root,root) %{_bindir}/mate-time-admin
%attr(755,root,root) %{_bindir}/mate-typing-monitor
%attr(755,root,root) %{_bindir}/mate-window-properties
%attr(755,root,root) %{_sbindir}/mate-display-properties-install-systemwide
%dir %{_libdir}/window-manager-settings
%attr(755,root,root) %{_libdir}/window-manager-settings/libmarco.so
%{_sysconfdir}/xdg/menus/matecc.menu
%{_datadir}/desktop-directories/matecc.directory
%{_datadir}/glib-2.0/schemas/org.mate.control-center*.gschema.xml
%dir %{_datadir}/mate-control-center
%dir %{_datadir}/mate-control-center/keybindings
%{_datadir}/mate-control-center/keybindings/00-multimedia-key.xml
%{_datadir}/mate-control-center/keybindings/01-desktop-key.xml
%{_datadir}/mate-control-center/pixmaps
%{_datadir}/mate-time-admin
%{_datadir}/mime/packages/mate-theme-package.xml
%{_datadir}/thumbnailers/mate-font-viewer.thumbnailer
%{_datadir}/polkit-1/actions/org.mate.randr.policy
%{_desktopdir}/mate-about-me.desktop
%{_desktopdir}/mate-appearance-properties.desktop
%{_desktopdir}/mate-at-properties.desktop
%{_desktopdir}/mate-default-applications-properties.desktop
%{_desktopdir}/mate-display-properties.desktop
%{_desktopdir}/mate-font-viewer.desktop
%{_desktopdir}/mate-keybinding.desktop
%{_desktopdir}/mate-keyboard.desktop
%{_desktopdir}/mate-network-properties.desktop
%{_desktopdir}/mate-settings-mouse.desktop
%{_desktopdir}/mate-theme-installer.desktop
%{_desktopdir}/mate-time-admin.desktop
%{_desktopdir}/mate-window-properties.desktop
%{_desktopdir}/matecc.desktop
%{_iconsdir}/hicolor/*x*/apps/mate-typing-monitor.png
%{_iconsdir}/hicolor/*x*/categories/instant-messaging.png
%{_iconsdir}/hicolor/scalable/apps/mate-typing-monitor.svg
%{_mandir}/man1/mate-about-me.1*
%{_mandir}/man1/mate-appearance-properties.1*
%{_mandir}/man1/mate-at-properties.1*
%{_mandir}/man1/mate-control-center.1*
%{_mandir}/man1/mate-default-applications-properties.1*
%{_mandir}/man1/mate-display-properties-install-systemwide.1*
%{_mandir}/man1/mate-display-properties.1*
%{_mandir}/man1/mate-font-viewer.1*
%{_mandir}/man1/mate-keybinding-properties.1*
%{_mandir}/man1/mate-keyboard-properties.1*
%{_mandir}/man1/mate-mouse-properties.1*
%{_mandir}/man1/mate-network-properties.1*
%{_mandir}/man1/mate-thumbnail-font.1*
%{_mandir}/man1/mate-typing-monitor.1*
%{_mandir}/man1/mate-window-properties.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmate-slab.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmate-slab.so.0
%attr(755,root,root) %{_libdir}/libmate-window-settings.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmate-window-settings.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmate-slab.so
%attr(755,root,root) %{_libdir}/libmate-window-settings.so
%{_includedir}/libmate-slab
%{_includedir}/mate-window-settings-2.0
%{_pkgconfigdir}/mate-default-applications.pc
%{_pkgconfigdir}/mate-keybindings.pc
%{_pkgconfigdir}/mate-slab.pc
%{_pkgconfigdir}/mate-window-settings-2.0.pc
