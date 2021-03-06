# HtPasswd file and Dokuwiki users authentication for TRAC

HtAndDokuPasswdStore aims to authenticate TRAC users with htpasswd files and
fallback to dokuwiki user accounts.

It is implemented as an extension to the TRAC plugin [AccountManager](https://trac-hacks.org/wiki/AccountManagerPlugin).

It does not allow to change user info in the web interface.

WARNING: supports only python crypt.crypt / md5 / sha1 password hashes

## Install

```
$ git clone cd htanddokupasswdstore
$ python setup.py bdist_egg
$ cp dist/TracHtAndDokuPasswdStore-0.5-py2.7.egg <your_trac_plugins_dir>
```

## Usage

To use it just configure your `trac.ini` like:

```
[components]
acct_mgr.db.SessionStore = enabled
acct_mgr.pwhash.htdigesthashmethod = enabled
acct_mgr.pwhash.htpasswdhashmethod = enabled
acct_mgr.api.AccountManager = enabled
acct_mgr.web_ui.LoginModule = enabled
trac.web.auth.LoginModule = disabled
htanddokupasswdstore.htfileanddokuauth.HtFileAndDokuAuthStore = enabled

[account-manager]
password_store = HtFileAndDokuAuthStore
htpasswd_hash_type =
htpasswd_file = /var/www/trac-envs/our.htpasswd
dokupasswd_file = /var/www/doku/conf/users.auth.php
reset_password = false
```
