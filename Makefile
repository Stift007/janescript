exec=compile
$(exec):
	
		echo "Downloading Compiler...";
		./build/pip install pyinstaller;
		pyinstaller --onefile main.py;
		mv dist/main ./jns;
		echo 'PATH=/usr/local/sbin:/usr/local/bin:/usr/bin:/usr/bin/site_perl:/usr/bin/vendor_perl:/usr/bin/core_perl:/home/forge/graw:/home/stormedjane/.local/bin:/home/stormedjane/nynx:/home/stormedjane/v:/home/stormedjane/JaneScript/Janescript' >> ~/.bashrc;
		echo 'JNSPATH="%/build/python3 /home/stormedjane/JaneScript/Janescript/main.py"' >> ~/.bashrc;
		    