# Get Coach Freq

This program takes a period (start date / end date) and a sport name as inputs and outputs the number of customers each coach had on this specific period and only for this specific sport.

## Getting started

The script is simple and consists of one simple python script file called 'main.py'

### Prerequisites

In order to make it work, you will need to have python 3 installed and the librairies in requirements.txt. You also need to have an access to the database.


### Installing

In order to retrieve the data, you need to install the ODBC driver for SQL Server:
- [Instructions for Windows](https://docs.microsoft.com/fr-fr/sql/connect/odbc/windows/microsoft-odbc-driver-for-sql-server-on-windows?view=sql-server-ver15) - [direct link to download page](https://docs.microsoft.com/fr-fr/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver15#download-for-windows)
- [Instructions for Linux and MacOs](https://docs.microsoft.com/fr-fr/sql/connect/odbc/linux-mac/system-requirements?view=sql-server-ver15)

Then install requirements.txt with pip, or another package manager.

```
pip install -r requirements.txt
```
### Connection to remote server

To access the data you must create a file named 'config.yaml' which follows this structure:

```
server: <server>
database: <database>
username: <username>
password: <password>
```

### Demonstration

You can start the program providing four arguments : startdate, enddate and sport. 

```
python main.py --startdate 2019-01-01 --enddate 2019-12-27 --sport zumba --output display 
```

### Arguments

- --startdate / --enddate : Date format is YYYY-MM-DD. Default argument is the entire 2019 year.
- --sport : Sport can be entered in upper case or lower case but has to match exactly to a sport name in database. Default argument is 'BODY COMBAT'.
- -- output:  Allows the user to choose the desired output type. Default is 'both' :
    - 'json' : exports the results to a json file called 'results.json'.
    - 'display': only displays the results in terminal.
    - 'both': exports to json and display the results.

### Local work

If you happen to have those tables stored in CSV files. You can set the global variable ``REMOTE`` to ``False``. In that case, script will try to read the .csv files and will not retrieve data from the distant server.

You can also use ``python main.py --help`` for more details.

## Authors

* **Virgile Pesce** - *Initial work* - [virgilus](https://github.com/virgilus)

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE - see the [LICENSE.md](LICENSE.md) file for details