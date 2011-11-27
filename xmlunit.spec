# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

Name:           xmlunit
Version:        1.3
Release:        6
Summary:        Provides classes to do asserts on xml
License:        BSD
Source0:        http://downloads.sourceforge.net/project/xmlunit/xmlunit%20for%20Java/XMLUnit%20for%20Java%201.3/xmlunit-1.3-src.zip
Source1:        http://repo1.maven.org/maven2/xmlunit/xmlunit/1.0/xmlunit-1.0.pom
URL:            http://xmlunit.sourceforge.net/
BuildRequires:  jpackage-utils >= 0:1.7.3
BuildRequires:  java-devel >= 0:1.6.0
BuildRequires:  ant >= 0:1.6.5
BuildRequires:  ant-junit
BuildRequires:  ant-trax
BuildRequires:  junit >= 0:3.8.1
BuildRequires:  xalan-j2
BuildRequires:  xerces-j2
BuildRequires:  xml-commons-apis
#BuildRequires:  dblatex
#BuildRequires:  docbook5-style-xsl
Requires:       junit >= 0:3.8
Requires:       xalan-j2
Requires:       xml-commons-apis
Requires:       jpackage-utils
Group:          Development/Java
BuildArch:      noarch

%description
XMLUnit extends JUnit to simplify unit testing of XML. It compares a control
XML document to a test document or the result of a transformation, validates
documents against a DTD, and (from v0.5) compares the results of XPath
expressions.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java
Requires:       jpackage-utils

%description    javadoc
Javadoc for %{name}

%prep
%setup -q 
# remove all binary libs and javadocs
find . -name "*.jar" -exec rm -f {} \;
rm -rf doc

cat >build.properties <<EOF
junit.lib=$(build-classpath junit)
xmlxsl.lib=$(build-classpath xalan-j2 xalan-j2-serializer xerces-j2)
test.report.dir=test
EOF

cat >docbook.properties <<EOF
db5.xsl=%{_datadir}/sgml/docbook/xsl-ns-stylesheets
EOF

#Fix wrong-file-end-of-line-encoding
sed -i 's/\r//g' README.txt LICENSE.txt

%build
export CLASSPATH=$(build-classpath xalan-j2-serializer)
ant -Dbuild.compiler=modern -Dfailonerror=false jar javadocs

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_javadir}
install -m 0644 build/lib/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
%add_to_maven_depmap %{name} %{name} %{version} JPP %{name}

# poms
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms

install -m 644 %{SOURCE1} \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP-%{name}.pom


# Javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/doc/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%{_javadir}/*
%doc README.txt LICENSE.txt userguide/XMLUnit-Java.pdf 
%{_datadir}/maven2/poms/*
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

