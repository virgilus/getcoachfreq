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

End with an example of getting some data out of the system or using it for a little demo

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

- --startdate / --enddate : Date format is YYYY-MM-DD.
- --sport : Sport can be entered in upper case or lower case but has to match exactly to a sport name in database.
- -- output:  Allows the user to choose the desired output type :
    - 'json' : export the results to a json file called 'results.json'.
    - 'display': only display the results in terminal
    - 'both': export to json and display the results

You can also use ``python main.py --help`` for more details.

## Authors

* **Virgile Pesce** - *Initial work* - [virgilus](https://github.com/virgilus)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details