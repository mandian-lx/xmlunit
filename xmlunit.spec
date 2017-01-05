Summary:	Testing and comparing XML output for Java and .NET
Name:		xmlunit
Version:	2.3.0
Release:	1
License:	ASL 2.0
Group:		Development/Java
URL:		https://www.xmlunit.org/
Source0:	https://github.com/%{name}/%{name}/releases/download/v%{version}/%{name}-%{version}-src.tar.bz2
BuildArch:	noarch

BuildRequires:	jpackage-utils
BuildRequires:	java-headless
BuildRequires:	maven-local
BuildRequires:	mvn(org.hamcrest:hamcrest-core)
BuildRequires:	mvn(org.hamcrest:hamcrest-library)
# The followings are required for tests only
BuildRequires:	mvn(junit:junit)
BuildRequires:	mvn(org.mockito:mockito-core)

Requires:	java-headless
Requires:	jpackage-utils

%description
XMLUnit is a library that supports testing XML output in several ways.

XMLUnit 2.x is a complete rewrite of XMLUnit and actually doesn't share
any code with XMLUnit for Java 1.x.

Some goals for XMLUnit 2.x:

 *  create .NET and Java versions that are compatible in design while trying
    to be idiomatic for each platform
 *  remove all static configuration (the old XMLUnit class setter methods)
 *  focus on the parts that are useful for testing
	XPath
	(Schema) validation
	comparisons
 *  be independent of any test framework

%files -f .mfiles
%doc RELEASE_NOTES.md
%doc CONTRIBUTING.md
%doc HELP_WANTED.md
%doc LICENSE
%doc KEYS

#----------------------------------------------------------------------------

%package javadoc
Summary:	Javadoc for %{name}

%description javadoc
API documentation for %{name}.

%files javadoc	-f .mfiles-javadoc
%doc LICENSE

#----------------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{version}-src

# Delete prebuild binaries
find . -name "*.jar" -delete
find . -name "*.class" -delete

# Remove failing plugin
%pom_rempve_plugin :buildnumber-maven-plugin

# Fix jar-not-indexed warning
%pom_xpath_inject "pom:plugin[pom:artifactId[./text()='maven-jar-plugin']]/pom:configuration/pom:archive" "
	<index>true</index>"

%build
%mvn_build

%install
%mvn_install

