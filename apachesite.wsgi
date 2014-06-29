<VirtualHost *:80>
		ServerName mywebsite.com
		ServerAdmin admin@mywebsite.com
		WSGIScriptAlias / /var/www/fedora-college/fedora_collge.wsgi
		<Directory /var/www/fedora-college/fedora_collge/>
			Order allow,deny
			Allow from all
		</Directory>
		Alias /static /var/www/fedora-college/fedora_collge/static
		<Directory /var/www/fedora-college/fedora_collge/static/>
			Order allow,deny
			Allow from all
		</Directory>
		ErrorLog ${APACHE_LOG_DIR}/error.log
		LogLevel warn
		CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>