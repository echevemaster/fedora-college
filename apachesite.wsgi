<VirtualHost *:80>
		ServerName mywebsite.com
		ServerAdmin admin@mywebsite.com
		WSGIScriptAlias / /home/engineer/fedora-college/fedora_college.wsgi
		<Directory /home/engineer/fedora-college/fedora_college/>
			Order allow,deny
			Allow from all
		</Directory>
		Alias /static /home/engineer/fedora-college/fedora_college/static
		<Directory /home/engineer/fedora-college/fedora_college/static/>
			Order allow,deny
			Allow from all
		</Directory>
		ErrorLog ${APACHE_LOG_DIR}/error.log
		LogLevel warn
		CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>