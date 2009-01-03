%define oname   Kiwi2

Summary:       A Framework for developing graphical applications in Python
Name:          python-%{oname}
Version:       1.9.0
Release:       %mkrel 6
Source:        %{oname}-%{version}.tar.bz2
License:       LGPL
Group:         Development/Python
BuildRoot:     %{_tmppath}/%{name}-buildroot
Url:           http://www.async.com.br/projects/kiwi
BuildRequires: python-devel
Requires:      pygtk2.0
BuildArch:     noarch

%description
Kiwi is a framework composed of a set of modules, which eases Python
development using PyGTK. Kiwi makes graphical applications *much* faster
to code, with good architecture and more Python-like bindings; it also
offers extended widgets based upon the original PyGTK widge


%package -n gazpacho-plugin-Kiwi2
Summary: This plugin allows you to use Kiwi2 Widgets from Gazpacho
Group: Development/Python
Requires: gazpacho >= 0.5.2

%description -n gazpacho-plugin-Kiwi2
This plugin allows you to use Kiwi2 Widgets from Gazpacho.


%prep
%setup -q -n %{oname}-%{version}
find . -name '.svn' | xargs rm -Rf 
# various perm fix
chmod og+r -R .
chmod og+x $(find . -type d)

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --root $RPM_BUILD_ROOT

pushd gazpacho-plugin

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/gazpacho/catalogs/pixmaps
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/gazpacho/pixmaps

python << EOF > kiwi2.xml.tmp
import re
import sys

resource_path_re = re.compile('resource-path="(\w|\d|/|-)+"')

for line in file("kiwi2.xml"):
	line = resource_path_re.sub('resource-path="%{_datadir}/gazpacho/catalogs"', line)
	sys.stdout.write(line)
EOF
install -m 644 kiwi2.xml.tmp $RPM_BUILD_ROOT/%{_datadir}/gazpacho/catalogs/kiwi2.xml
install -m 644 kiwi2.py $RPM_BUILD_ROOT/%{_datadir}/gazpacho/catalogs

for pixmap in pixmaps/*
do
	install -m 644 $pixmap $RPM_BUILD_ROOT/%{_datadir}/gazpacho/catalogs/pixmaps
done

popd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING README doc examples tests
%py_puresitedir/Kiwi2
%py_puresitedir/*.egg-info

%files -n gazpacho-plugin-Kiwi2
%defattr(-,root,root)
%{_datadir}/gazpacho/catalogs/kiwi2.xml
%{_datadir}/gazpacho/catalogs/kiwi2.py
%{_datadir}/gazpacho/catalogs/pixmaps/kiwi*.png


