Summary:	Displays the users logged into machines on the local network
Name:		rusers
Version:	0.17
Release:	31
License:	BSD
Group:		Monitoring
Url:		ftp://sunsite.unc.edu/pub/Linux/system/network/daemons/
Source0:	ftp://sunsite.unc.edu/pub/Linux/system/network/daemons/netkit-rusers-%{version}.tar.bz2
Source1:	rusersd.service
Source2:	rstatd.tar.bz2
Source3:	rstatd.service
Source4:	rusers.x
Source5:	rstat.x
Source100:	rusers.rpmlintrc
Patch0:		rstatd-jbj.patch
Patch1:		netkit-rusers-0.15-numusers.patch
Patch2:		rusers-0.15-libproc.patch
Patch3:		netkit-rusers-0.17-2.4.patch
Patch4:		netkit-rusers-0.17-includes.patch
Patch5:		netkit-rusers-0.17-2.6-stats.patch
BuildRequires:	pkgconfig(libprocps)
BuildRequires:	pkgconfig(libtirpc)

%description
The rusers program allows users to find out who is logged into various machines
on the local network.  The rusers command produces output similar to who, but
for the specified list of hosts or for all machines on the local network.

Install rusers if you need to keep track of who is logged into your local
network.

%files
%{_bindir}/rup
%{_bindir}/rusers
%{_mandir}/man1/*

#----------------------------------------------------------------------------

%package	server
Summary:	Server for the rusers protocol
Group:		System/Servers
Requires:	rpcbind

%description	server
The rusers program allows users to find out who is logged into various machines
on the local network. The rusers command produces output similar to who, but
for the specified list of hosts or for all machines on the local network. The
rusers-server package contains the server for responding to rusers requests.
(rpc.rusersd, rpc.rstatd)

Install rusers-server if you want remote users to be able to see who is logged
into your machine.

%files server
%doc  README ChangeLog BUGS
%{_unitdir}/*
%{_sbindir}/*
%{_mandir}/man8/*

#----------------------------------------------------------------------------

%prep
%setup -qn netkit-rusers-%{version} -a 2
cp %{SOURCE4} %{SOURCE5} .
%apply_patches

%build
%serverbuild
sh configure
sed -i -e 's|-O2|\$(RPM_OPT_FLAGS)|' MCONFIG
sed -i -e 's|LIBS=|LIBS=-ltirpc|' MCONFIG
sed -i -e 's|/usr/include/rpcsvc/rusers.x|../rusers.x|g' */Makefile
sed -i -e 's|/usr/include/rpcsvc/rstat.x|../rstat.x|g' */*akefile

%make
%make -C rpc.rstatd

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_mandir}/{man1,man8}

make INSTALLROOT=%{buildroot} install MANDIR=%{_mandir}
make INSTALLROOT=%{buildroot} install -C rpc.rstatd MANDIR=%{_mandir}

install -m 755 %{SOURCE1} %{buildroot}%{_unitdir}/rusersd.service
install -m 755 %{SOURCE3} %{buildroot}%{_unitdir}/rstatd.service

cd %{buildroot}%{_mandir}/man8
for i in rstatd rusersd; do
	rm $i.8
	ln -s rpc.$i.8.bz2 $i.8.bz2
done

