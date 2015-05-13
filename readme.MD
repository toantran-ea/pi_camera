Setup Dropbox app to authenticate Pi access:
====
You will need to create an app on Dropbox (https://www.dropbox.com/developers/apps)
* Create new Dropbox app from above link.
* Generate your access token:
![alt tag](https://www.dropbox.com/s/lu1a3wehdppia7x/Screenshot%202015-05-13%2014.05.13.png?dl=1)
* Create file `token-store.txt` (same place with `pi_con.py`) with following format:
```
oauth2:YOUR_TOKEN_GOES_HERE
```

Work with raspberry pi module
====
* take picture periodically. (Done + save to local storage)
* sync pics with dropbox.
* receive simple commands from outsite controller devices.


To run on Raspberry Pi in background, use:
``` nohup python pi_cron.py > output.txt & ```

