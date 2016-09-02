
MSG_PREFIX="\n#Please install"
MSG_SUFFIX="\n\n=) See you later...\n"

if ! [ $(id -u) = 0 ]; then
   echo "This script must be run as root" 
   echo -e $MSG_SUFFIX
   exit 1
fi

DEP_PROBLEM=0
command -v pip >/dev/null 2>&1 || { echo -e >&2 "$MSG_PREFIX pip\n More information: http://pip.pypa.io/en/latest/installing.html"; DEP_PROBLEM=1; }
command -v openssl >/dev/null 2>&1 || { echo -e >&2 "$MSG_PREFIX openssl\n Try one of these comands:\n  sudo apt-get install openssl\n  sudo yum install openssl"; DEP_PROBLEM=1; }

if [ $DEP_PROBLEM -eq 1 ]; then
	echo -e $MSG_SUFFIX
	exit
fi

for pkg in "google-api-python-client" 'pyOpenSSL>=0.11' "pyCrypto" "earthengine-api" "wget" "pyshp" "scipy"; do
	echo "#### INSTALLING $pkg..."
	pip install --upgrade "$pkg"
done