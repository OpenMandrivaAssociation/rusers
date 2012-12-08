Summary:	Displays the users logged into machines on the local network
Name:		rusers
Version:	0.17
Release: 	%mkrel 24
License:	BSD
Group:		Monitoring
URL:		ftp://sunsite.unc.edu/pub/Linux/system/network/daemons/
Source:		ftp://sunsite.unc.edu/pub/Linux/system/network/daemons/netkit-rusers-%{version}.tar.bz2
Source1:	rusersd.init
Source2:	rstatd.tar.bz2
Source3:	rstatd.init
Patch0:		rstatd-jbj.patch
Patch1:		netkit-rusers-0.15-numusers.patch
Patch2:		rusers-0.15-libproc.patch
Patch3:		netkit-rusers-0.17-2.4.patch
Patch4:		netkit-rusers-0.17-includes.patch
Patch5:		netkit-rusers-0.17-2.6-stats.patch
BuildRequires:	procps-devel
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root

%description
The rusers program allows users to find out who is logged into various machines
on the local network.  The rusers command produces output similar to who, but
for the specified list of hosts or for all machines on the local network.

Install rusers if you need to keep track of who is logged into your local
network.

%package	server
Summary:	Server for the rusers protocol
Group:		System/Servers
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires:	rpcbind

%description	server
The rusers program allows users to find out who is logged into various machines
on the local network. The rusers command produces output similar to who, but
for the specified list of hosts or for all machines on the local network. The
rusers-server package contains the server for responding to rusers requests.
(rpc.rusersd, rpc.rstatd)

Install rusers-server if you want remote users to be able to see who is logged
into your machine.

%prep

%setup -q -n netkit-rusers-%{version} -a 2
%patch0 -p1 -b .jbj
%patch1 -p1 -b .numusers
%patch2 -p1 -b .warly
%patch3 -p1 -b .mdk
%patch4 -p1 -b .mdk
%patch5 -p1 -b .2.6-stats

%build
%serverbuild
sh configure
perl -pi -e 's,-O2,\$(RPM_OPT_FLAGS),' MCONFIG

%make
%make -C rpc.rstatd

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}%{_mandir}/{man1,man8}

make INSTALLROOT=%{buildroot} install MANDIR=%{_mandir}
make INSTALLROOT=%{buildroot} install -C rpc.rstatd MANDIR=%{_mandir}

install -m 755 %SOURCE1 %{buildroot}%{_initrddir}/rusersd
install -m 755 %SOURCE3 %{buildroot}%{_initrddir}/rstatd

cd %{buildroot}%{_mandir}/man8
for i in rstatd rusersd; do
	rm $i.8
	ln -s rpc.$i.8.bz2 $i.8.bz2
done

perl -pi -e "s|/etc/rc.d/init.d|%{_initrddir}|" %{buildroot}%{_initrddir}/*

%clean
rm -rf %{buildroot}

%post server
%_post_service rusersd
%_post_service rstatd

%preun server
%_preun_service rusersd
%_preun_service rstatd

%files
%defattr(-,root,root)
%{_bindir}/rup
%{_bindir}/rusers
%{_mandir}/man1/*

%files server
%defattr(-,root,root)
%doc  README ChangeLog BUGS
%{_initrddir}/rusersd
%{_initrddir}/rstatd
%{_mandir}/man8/*
%{_sbindir}/*




%changelog
* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 0.17-22mdv2011.0
+ Revision: 669464
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0.17-21mdv2011.0
+ Revision: 607384
- rebuild

* Mon Mar 15 2010 Oden Eriksson <oeriksson@mandriva.com> 0.17-20mdv2010.1
+ Revision: 520211
- rebuilt for 2010.1

* Sun Jul 26 2009 Guillaume Rousse <guillomovitch@mandriva.org> 0.17-19mdv2010.0
+ Revision: 400288
- fixw dependencies

* Fri Dec 19 2008 Oden Eriksson <oeriksson@mandriva.com> 0.17-18mdv2009.1
+ Revision: 316187
- rebuild

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 0.17-17mdv2009.0
+ Revision: 225341
- rebuild

* Wed Mar 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.17-16mdv2008.1
+ Revision: 179478
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Sat Mar 17 2007 Oden Eriksson <oeriksson@mandriva.com> 0.17-15mdv2007.1
+ Revision: 145572
- Import rusers

* Sat Mar 17 2007 Oden Eriksson <oeriksson@mandriva.com> 0.17-15mdv2007.1
- use the %%mrel macro
- bunzip patches

* Thu Mar 23 2006 Gwenole Beauchesne <gbeauchesne@mandriva.com> 0.17-14mdk
- fix rpc.rstatd for 2.6 kernels...

* Sun Jan 01 2006 Mandriva Linux Team <http://www.mandrivaexpert.com/> 0.17-13mdk
- Rebuild

* Fri Feb 25 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.17-12mdk
- rebuild for new libproc

* Sat May 15 2004 Nicolas Planel <nplanel@mandrakesoft.com> 0.17-11mdk
- rebuild fot cooker.

