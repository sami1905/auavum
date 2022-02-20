# auavum

## Step 1 — Installing the Components from the Ubuntu Repositories

The first step is to install all of the necessary packages from the default Ubuntu repositories:
```console
$ sudo apt update
```

Then install the packages that will allow you to build your Python environment:
```console
$ sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
```

## Step 2 — Creating a Python Virtual Environment

Start by installing the python3-venv package, which will install the venv module:
```console
$ sudo apt install python3-venv
```

Next, make a parent directory for your project:
```console
$ mkdir ~/myproject
```

Then change into the directory after you create it:
```console
$ cd ~/myproject
```

Create a virtual environment to store your project’s Python requirements by entering the following:
```console
$ python3.6 -m venv myprojectenv
```

Before installing applications within the virtual environment, you need to activate it by running the following:
```console
$ source myprojectenv/bin/activate
```

Your prompt will change to indicate that you are now operating within the virtual environment. It will read like the following:
```console
$ (myprojectenv)\s<hostname>:~/myproject$
```

## Step 3 — Setting Up the Application
Now that you are in your virtual environment, you can install Dash and Gunicorn and get started on designing your application.

First, install wheel with the local instance of pip to ensure that your packages will install even if they are missing wheel archives:
```console
(myprojectenv)\s$ pip install wheel
```
Next, install Dash and Gunicorn:```console
(myprojectenv)\s$ pip install gunicorn dash
```

While your application might be more complex, we’ll create our Dash application in two files, called app.py and index.py. Create this file using your preferred text editor; here we’ll use nano:
```console
(myprojectenv)\s$ nano ~/myproject/app.py
```
```console
(myprojectenv)\s$ nano ~/myproject/index.py
```

```python
app.py

import dash

app = dash.Dash(__name__)

server = app.server
```

```python
index.py

#connect to main app.py file and to apps
from app import app, server
from dash import html

app.layout = dbc.Container([
    html.P('Hello there!'),
], className='content', fluid=True)

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True, port='5000')
```

If you followed the initial server setup guide in the prerequisites, you should have a UFW firewall enabled. To test the application, first you need to allow access to port 5000:
```console
(myprojectenv)\s$ sudo ufw allow 5000
```

Then you can test your Dash application by running the following:
```console
(myprojectenv)\s$ python index.py
```

## Step 4 — Configuring Gunicorn
Your application is now written with an entry point established and you can proceed to configuring Gunicorn.

But first, change into to the appropriate directory:
```console
(myprojectenv)\s$ cd ~/myproject
```

Next, you can check that Gunicorn can serve the application correctly by passing it the name of your entry point. This is constructed as the name of the module (minus the .py extension), plus the name of the callable within the application. In our case, this is written as index:server.

You’ll also specify the interface and port to bind to so that the application will be started on a publicly available interface:
```console
(myprojectenv)\s$ gunicorn index:server --b 0.0.0.0:5000
```

Since now you’re done with your virtual environment, deactivate it:
```console
(myprojectenv)\s$ deactivate
```

Any Python commands will now use the system’s Python environment again.

Next, create the systemd service unit file. Creating a systemd unit file will allow Ubuntu’s init system to automatically start Gunicorn and serve the Dash application whenever the server boots.

Create a unit file ending in .service within the /etc/systemd/system directory to begin:
```console
$ sudo nano /etc/systemd/system/myproject.service
```

```
[Unit]
Description=Gunicorn instance to serve myproject
After=network.target

[Service]
User=<hostname>
Group=www-data
WorkingDirectory=/home/<hostname>/myproject
Environment="PATH=/home/<hostname>/myproject/myprojectenv/bin"
ExecStart=/home/<hostname>/myproject/myprojectenv/bin/gunicorn --workers 3 --bind unix:myproject.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
```

With that, your systemd service file is complete. Save and close it now.

Now start the Gunicorn service you created:
```console
$ systemctl start myproject
```

Then enable it so that it starts at boot:
```console
$ systemctl enable myproject
```

Check the status:
```console
$ systemctl status myproject
```

You should receive output like the following:
```
myproject.service - Gunicorn instance to serve myproject
   Loaded: loaded (/etc/systemd/system/myproject.service; enabled; vendor preset
   Active: active (running) since Fri 2021-11-19 23:08:44 UTC; 6s ago
 Main PID: 8770 (gunicorn)
    Tasks: 4 (limit: 1151)
   CGroup: /system.slice/myproject.service
       	├─9291 /home/sammy/myproject/myprojectenv/bin/python3.6 /home/sammy/myproject/myprojectenv/bin/gunicorn --workers 3 --bind unix:myproject.sock -m 007 wsgi:app
       	├─9309 /home/sammy/myproject/myprojectenv/bin/python3.6 /home/sammy/myproject/myprojectenv/bin/gunicorn --workers 3 --bind unix:myproject.sock -m 007 wsgi:app
       	├─9310 /home/sammy/myproject/myprojectenv/bin/python3.6 /home/sammy/myproject/myprojectenv/bin/gunicorn --workers 3 --bind unix:myproject.sock -m 007 wsgi:app
       	└─9311 /home/sammy/myproject/myprojectenv/bin/python3.6 /home/sammy/myproject/myprojectenv/bin/gunicorn --workers 3 --bind unix:myproject.sock -m 007 wsgi:app
…
```

## Step 5 — Configuring Nginx to Proxy Requests
Your Gunicorn application server should now be up and running, waiting for requests on the socket file in the project directory. Next, configure Nginx to pass web requests to that socket by making some small additions to its configuration file.

Begin by creating a new server block configuration file in Nginx’s sites-available directory. We’ll call this myproject to stay consistent with the rest of the guide:
```console
$ sudo nano /etc/nginx/sites-available/myproject
```
```console
$ sudo nano /etc/nginx/sites-enabled/myproject
```
```console
$ sudo nano /etc/nginx/sites-available/default
```

Open up a server block and tell Nginx to listen on the port 443. Also, tell it to use this block for requests for your server’s domain name:
```
server {
    listen 443 ssl default_server;
    listen [::]:443 ssl default_server;

    ssl_certificate /etc/nginx/certificate/ssl.crt;
    ssl_certificate_key /etc/nginx/certificate/nginx.key;
    root /var/www/html;

    server_name _;

    location / {
        include     proxy_params;
        proxy_pass  "http://10.10.83.28:5000/";
    }
}
```
To enable the Nginx server block configuration you’ve created, link the file to the sites-enabled directory. You can do this by running the ln command and the -s flag to create a symbolic or soft link, as opposed to a hard link:
```console
$ sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled
```

With the link in that directory, you can test for syntax errors:
```console
$ sudo nginx -t
```

If this returns without indicating any issues, restart the Nginx process to read the new configuration:
```console
$ sudo systemctl restart nginx
```
```console
$ sudo systemctl daemon-reload
```
```console
$ sudo systemctl daemon-reexec
```

Finally, adjust the firewall again. Since you no longer need access through port 5000, remove that rule:
```console
$ sudo ufw allow 'Nginx Full'
```

You should now be able to navigate to your server’s domain name in your web browser:
```console
$ gunicorn index:server --b 0.0.0.0:5000
```

Kill gunicorn:
```console
$ pkill gunicorn
```