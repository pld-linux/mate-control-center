Summary:	MATE Desktop control-center
Name:		mate-control-center
Version:	1.5.2
Release:	0.1
License:	LGPLv2+ and GPLv2+
URL:		http://mate-desktop.org/
Source0:	http://pub.mate-desktop.org/releases/1.5/%{name}-%{version}.tar.xz
# Source0-md5:	265cff2fa1b3c1c4232bb1743d079c73
Group:		X11/Applications
BuildRequires:	desktop-file-utils
BuildRequires:	icon-naming-utils
BuildRequires:	mate-common
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(dconf)
BuildRequires:	pkgconfig(gsettings-desktop-schemas)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(libcanberra)
BuildRequires:	pkgconfig(libmarco-private)
BuildRequires:	pkgconfig(libmate-menu)
BuildRequires:	pkgconfig(libmatekbd)
BuildRequires:	pkgconfig(libmatenotify)
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(libxklavier)
BuildRequires:	pkgconfig(mate-desktop-2.0)
BuildRequires:	pkgconfig(mate-doc-utils)
BuildRequires:	pkgconfig(mate-settings-daemon)
BuildRequires:	pkgconfig(nss)
BuildRequires:	pkgconfig(polkit-agent-1)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(unique-1.0)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xkbfile)
BuildRequires:	pkgconfig(xscrnsaver)
BuildRequires:	pkgconfig(xxf86misc)
BuildRequires:	rpmbuild(macros) >= 1.596
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	desktop-file-utils
Requires:	glib2 >= 1:2.26.0
Requires:	gsettings-desktop-schemas
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
Requires:	shared-mime-info
Requires(post,postun):	/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MATE Desktop Control Center

%package -n libslab
Summary:	MATE Desktop libslab port
License:	LGPL v2+
Group:		Libraries

%description -n libslab
This package provides libslab which is used in MATE control panel and
in gnome-main-menu.

%package devel
Summary:	Development files for mate-settings-daemon
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

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

desktop-file-install \
	--remove-category="MATE" \
	--add-category="X-Mate" \
	--delete-original \
	--dir=$RPM_BUILD_ROOT%{_desktopdir} \
$RPM_BUILD_ROOT%{_desktopdir}/*.desktop

# delete mime cache
%{__rm} $RPM_BUILD_ROOT%{_desktopdir}/mimeinfo.cache

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_desktop_database
%update_icon_cache hicolor
%update_mime_database
%glib_compile_schemas

%postun
/sbin/ldconfig
%update_desktop_database_postun
%update_icon_cache hicolor
%update_mime_database
%glib_compile_schemas

%post	-n libslab -p /sbin/ldconfig
%postun	-n libslab -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING README
%{_sysconfdir}/xdg/menus/matecc.menu
%attr(755,root,root) %{_bindir}/mate-*
%attr(755,root,root) %{_sbindir}/mate-display-properties-install-systemwide
%attr(755,root,root) %{_libdir}/libmate-window-settings.so.*.*.*
%ghost %{_libdir}/libmate-window-settings.so.1
%dir %{_libdir}/window-manager-settings
%attr(755,root,root) %{_libdir}/window-manager-settings/libmarco.so
%{_desktopdir}/*.desktop
%{_datadir}/desktop-directories/matecc.directory
%{_iconsdir}/hicolor/*/apps/*.png
%{_iconsdir}/hicolor/scalable/apps/mate-*.svg
%{_datadir}/glib-2.0/schemas/org.mate.*.xml
%{_datadir}/mate-control-center
%{_datadir}/mate/cursor-fonts/*.pcf
%{_datadir}/mate/help/mate-control-center
%{_datadir}/mime/packages/mate-theme-package.xml
%{_datadir}/thumbnailers/mate-font-viewer.thumbnailer
%{_datadir}/omf/mate-control-center
%{_datadir}/polkit-1/actions/org.mate.randr.policy

# XXX proper package
%dir %{_datadir}/mate/cursor-fonts

%files -n libslab
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libslab.so.*.*.*
%ghost %{_libdir}/libslab.so.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libmate-window-settings.so
%{_includedir}/mate-window-settings-2.0
%{_pkgconfigdir}/mate-window-settings-2.0.pc
%{_npkgconfigdir}/mate-default-applications.pc
%{_npkgconfigdir}/mate-keybindings.pc

# libslab
%{_libdir}/libslab.so
%{_includedir}/libslab
%{_pkgconfigdir}/libslab.pc
