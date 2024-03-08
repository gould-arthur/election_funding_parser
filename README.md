## Election Funding Parser

### Overview
Election Funding Parser (EFP) aims to creates a lightweight tool for looking through donations made for elections and primaries in the years 1980-2014. Current functionality is limited to the downloading of a compessed file, parsing of that file, and storing into a database.


### Current Usage
The tool is in it's early stages of developement (see Future Fucntionality section), and currently only supports the creation of the database, specified via code. EFP aims to ensure that all end user interactions are as simple and minimal as possible. Currently, the only supported interaction is via command line and python code (Interacting through code)

### Command Line Interface
```
usage: efp_cli.py [-h] -y YEAR [-o OUTPUT_DB] [-i] [-c] [-l]

optional arguments:
  -h, --help            show this help message and exit
  -y YEAR, --year YEAR  year between 1980 and 2014 to parse data
  -o OUTPUT_DB, --output_db OUTPUT_DB
                        filename to store database as
  -i, --ignore_existing
                        set flag to ignore existing files and download regardless of whether or not files exist
  -c, --clean           When set, program will remove all created files aside from the log file
  -l, --lower-memory    flag to signify that device has lower memory. Will result in slower execution
```
The only required flag is "-y" to specify the year to populate into the database. Currently, only years 1980-2014 are supported.  
Example for calling with default values: ```> python3 efp_cli.py -y 1980```  
This line will result in downloading the gzipped file of 1980 donations from dataverse.harvard.edu, extracting the data and writing information to a database named "base_populated.db"  
  
Example for specifying low memory: ```>python3 efp_cli.py -y 1980 -l```  
This will ensure that the default process of holding as much data in memory as possible is not followed. This will often result in slower processing speeds. With smaller datasets, the run-time can be roughly equivalent or faster than the default. However, on larger sets, specifying "-l" will time-to-completion several times over.  
  
Example for clean: ```>python3 efp_cli.py -y 1980 -c```  
Setting the clean flag results in all but the downloaded file being deleted after running. This is mainly used for testing functionality and imports are working. The Downloaded data file will not be removed. \
\
Example for ignore existing: ```>python3 efp_cli.py -y 1980 -i```  
Setting this flag tells the application to download the desired gzipped data file, even if it already exists.\
\
Example for output_db: ```>python3 efp_cli.py -y 1980 -o new.db```  
Specifying the output name will overwrite the default filename "base_populated.db" as the sql database destingation. In this case, it would be names "new.db"


#### Interacting through code
EFP's Populator object uses the with-open format
```python
from efp_populator import Populator

with Populator() as p:
    p.populate(2000)  # populates the database with information from the year 2000
```
And the open-close format
```python
from efp_populator import Populator

p = Populator()
p.open()
p.populate(2000)
p.close()
```

### Future Functionality
- Breakout of singular table into improved scheme
- Using Django, provide web-interface for parsing data
- Create install for required libraries and dependencies
- Containerize application using Docker
- Expand available datasets to include 2016-2024

### Known Issues
Data cleaning is not yet 100%, resulting in malformed lines to be logged. Malformed lines are not added to the database at this time


#### Citation
Data downloaded and parsed is made available by:
    Bonica, Adam, 2015, "Database on Ideology, Money in Politics, and Elections (DIME)", https://doi.org/10.7910/DVN/O5PX0B, Harvard Dataverse, V3