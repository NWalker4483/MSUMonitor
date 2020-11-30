# MSUMonitor

Automatically monitor and register for courses when availabilities arise
## Setup
For the most recent version of the code please run
```git clone https://github.com/NWalker4483/MSUMonitor```

To deploy locally create an ```auth.py``` in the root dir with the contents ...

``` python
# Provide your own Websis Student Login
username = "*********"
password = "*********"
```
* Run ```python3 -m pip install -r requirements.txt```
## Deployment
* Run the start.sh script or run ```python3 server.py```
* Go to [localhost:5000](http://localhost:5000) in your choice of browser.

A production deployment can also be accessed through [msu-register.glitch.me](https://msu-register.glitch.me)
## Usage 
For frontend use instructions please refer to the user manual in the [docs](docs/) folder

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)