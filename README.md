## Election Funding Parser

### Overview
Election Funding Parser (EFP) aims to creates a lightweight tool for looking through donations made for elections and primaries in the years 1980-2014. Current functionality is limited to the downloading of a compessed file, parsing of that file, and storing into a database.


### Current Usage
The tool is in it's early stages of developement (see Future Fucntionality section), and currently only supports the creation of the database, specified via code. EFP aims to ensure that all end user interactions are as simple and minimal as possible. Currently, the only supported interaction is via python code (Interacting through code)

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
- CommandLine interface to pull specific year data into database
- Breakout of singular table into improved scheme
- Using Django, provide web-interface for parsing data
- Create install for required libraries and dependencies
- Containerize application using Docker

#### Citation
Data downloaded and parsed is made available by:
    Bonica, Adam, 2015, "Database on Ideology, Money in Politics, and Elections (DIME)", https://doi.org/10.7910/DVN/O5PX0B, Harvard Dataverse, V3