%define		dictname mueller7
Summary:	English-Russian dictionary for dictd
Summary(pl):	S³ownik angielsko-rosyjski dla dictd
Name:		dict-%{dictname}
Version:	1.2
Release:	4
License:	GPL
Group:		Applications/Dictionaries
Source0:	http://mueller-dic.chat.ru/Mueller7GPL.tgz
# Source0-md5:	0b3cd75e916f078b2caa4f2dc59508e4
# This one is compressed with bzip2 (do not trust tgz!)
#Source0:	http://www.geocities.com/mueller_dic/Mueller7GPL.tgz
Source1:	http://www.math.sunysb.edu/~comech/tools/to-dict
# Source1-md5:	3c1b69c290fb4c06bf3456baf5bf8b97
URL:		http://mueller-dic.chat.ru/
BuildRequires:	dictfmt
BuildRequires:	dictzip
%if "%(locale -a | grep '^ru_RU.koi8r$')" == ""
BuildRequires:	glibc-localedb-all
%endif
BuildRequires:	sed >= 4.0
Requires:	dictd
Requires:	%{_sysconfdir}/dictd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Electronic version of 7th edition of English-Russian dictionary by V.
K. Mueller.

%description -l pl
Elektroniczna wersja 7. wydania s³ownika angielsko rosyjskiego V. K.
Muellera.

%prep
%setup -q -c

cp %{SOURCE1} .
sed -i -e 's/dictfmt -p/dictfmt --locale ru_RU.koi8r -p/' to-dict

%build
chmod +x ./to-dict
./to-dict --no-trans usr/local/share/dict/Mueller7GPL.koi mueller7.notr
./to-dict --src-data mueller7.notr mueller7.data && rm -f mueller7.notr
./to-dict --data-dict mueller7.data mueller7 && rm -f mueller7.data
./to-dict --expand-index mueller7.index mueller7.index.exp
mv -f mueller7.index.exp mueller7.index

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/dictd,%{_sysconfdir}/dictd}

dictprefix=%{_datadir}/dictd/%{dictname}
echo "# Mueller English-Russian dictionary, 7-th edition (%{version})
database %{dictname} {
	data  \"$dictprefix.dict\"
	index \"$dictprefix.index\"
}" > $RPM_BUILD_ROOT%{_sysconfdir}/dictd/%{dictname}.dictconf
mv %{dictname}.* $RPM_BUILD_ROOT%{_datadir}/dictd

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/dictd ]; then
	/etc/rc.d/init.d/dictd restart 1>&2
fi

%postun
if [ -f /var/lock/subsys/dictd ]; then
	/etc/rc.d/init.d/dictd restart 1>&2 || true
fi

%files
%defattr(644,root,root,755)
%doc usr/local/share/mova/Mueller7.txt
%lang(ru) %doc usr/local/share/mova/Mueller7_koi.txt
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/dictd/%{dictname}.dictconf
%{_datadir}/dictd/%{dictname}.*
