**`PURPOSE`**:
This is an example of how you would programmatically dump information
from Plutora.

**`IMPLEMENTATION`**
Programmed in Python, using the requests library, this program
takes commandline parameters of the form 
    'python plutoraDump.py -p URL-suffix -f mycredentials.cfg'

Where URL-suffix is a path to the object of interest, for example, /systems

All user/password parameters are obtained from the config-file
named credentials.cfg, by default.  The file format is JSON:

```{
	"credentials": {
		"client_id": "XXXXXXXXXXXXXXX",
		"client_secret": "XXXXXXXXXXXXXXX",
		"username": "me@example.com",
		"password": "secretValue"
	}
}```


	1.5.17-jps
