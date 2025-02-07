#
# spec file for package discord-canary
#
# Copyright (c) 2018 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


# Require bash for extglob in install section.
%define shortname discord-canary
%global _buildshell /bin/bash
%global __requires_exclude ^(libffmpeg|libvulkan|libGLES|libEGL|libnode).*
%global __provides_exclude ^(libffmpeg|libvulkan|libGLES|libEGL|libnode).*
Name:           discord-canary
Version:        0.0.162
Release:        1
Summary:        Voice and Text Chat for Gamers
License:        SUSE-NonFree
Group:          Amusements/Games/Other
Url:            https://discordapp.com/
#Source0:        https://dl-canary.discordapp.net/apps/linux/%{version}/%{name}-%{version}.tar.gz
Source1:        discord-canary.desktop
#Source0:        https://zuhhaga.github.io/version_update/discord_canary.html#/%{name}.tar.gz
Source0:       https://discordapp.com/api/download/canary?platform=linux&format=tar.gz#/%{name}.tar.gz
ExclusiveArch:  x86_64
BuildRequires:  desktop-file-utils
BuildRequires:  hicolor-icon-theme
BuildRequires:  (update-desktop-files or unzip)
BuildRequires:  unzip
%define shortname discord-canary
## BOO#1191555 - libc++1 does not exist in TW anymore. Let's just do proper automatic dependencies instead of all this.
##Requires:       libgtk-2_0-0 libnotify-tools libasound2 gconf2 mozilla-nss dbus-1-glib libXtst6 libX11-6 libstdc++6 libc++1 libatomic1
# jap/kr/emote font support
Recommends:		noto-sans-kr-fonts noto-sans-jp-fonts noto-sans-cjk-fonts


%description
Discord is a voice and text chat for gamers. The Text chat supports
inline images and videos. Voice chat includes a jitter buffer,
automatic gain control, noise suppression, echo cancellation.
Server-to-client communications are encrypted.

%prep
%setup -n DiscordCanary

%build

%install
cd %{_builddir}/DiscordCanary
install -Dm644 discord.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{shortname}.png
desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE1}

install -Dm755 libffmpeg.so %{buildroot}%{_libdir}/%{shortname}/libffmpeg.so
install -Dm755 libEGL.so %{buildroot}%{_libdir}/%{shortname}/libEGL.so
install -Dm755 libGLESv2.so %{buildroot}%{_libdir}/%{shortname}/libGLESv2.so

# install share
mkdir -p %{buildroot}%{_libdir}/%{shortname}
shopt -s extglob
cp -r !(discord*|*.so) %{buildroot}%{_libdir}/%{shortname}
shopt -u extglob

# Executable checks for resources in its directory so it cannot be in bin.
mkdir -p %{buildroot}%{_bindir}
ln -s %{_libdir}/%{shortname}/DiscordCanary %{buildroot}%{_bindir}/%{shortname}

# fix missing icon in some envoronments
ln -sf %{_datadir}/icons/hicolor/256x256/apps/%{shortname}.png %{buildroot}%{_libdir}/%{shortname}/discord.png


%post
%if %{defined desktop_database_post}
%desktop_database_post
%endif
chmod 0755 %{_libdir}/%{shortname}/DiscordCanary

%postun
%if %{defined desktop_database_postun}
%desktop_database_postun
%endif

%files
%defattr(-,root,root)
%{_bindir}/%{shortname}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/256x256/apps/%{shortname}.png
%{_libdir}/%{shortname}

%changelog
