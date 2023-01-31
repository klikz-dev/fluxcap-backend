# fluxcap-backend

## Apache2 config

- sudo nano /etc/apache2/sites-available/000-default.conf

<VirtualHost \*:80>

    Alias /static /home/ubuntu/fluxcap/static
    <Directory /home/ubuntu/fluxcap/static>
        Require all granted
    </Directory>

    <Directory /home/ubuntu/fluxcap/admin>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

    WSGIDaemonProcess fluxcap python-path=/home/ubuntu/fluxcap python-home=/home/ubuntu/fluxcapenv
    WSGIProcessGroup fluxcap
    WSGIScriptAlias / /home/ubuntu/fluxcap/admin/wsgi.py

</VirtualHost>
