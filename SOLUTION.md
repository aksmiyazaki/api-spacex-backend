## How do I run this thing?
Let's get to the action right away.  
There's a Makefile in the project, you may run `make help` in order to see which commands are implemented.  
If you will run this on your local machine, I advise you to create a Python Virtual Environment in order to avoid 
installing stuff into your base Python installation.  
This was coded on a Mac with M1, to avoid incompatibilities, running the dockerized version of things is advised.

### Query
To fetch the last known position of a satellite by id and T, the query used is this one:
```
SELECT *
FROM   satellite
WHERE  satellite_id = '$(id_to_fetch)'
       AND creation_date < '$(creation_date)'
ORDER  BY creation_date DESC
LIMIT  1; 
```
Keep in mind that `id_to_fetch` and `creation_date` are placeholders.
To query the database you may execute something like:
```
make query-local id_to_fetch='5eed7714096e590006985694' creation_date='2021-01-26 06:26:11' 
```


## Brief Description
This is the solution of the proposed problem.  
I wasn't able to do the Bonus Task just because I was really loaded with work, sorry about that.    
I opted to deliver the simple version very well-rounded.
The solution is coded in Python, there is a significant coverage of tests in each part of the code excluding the glue
code of `main`.  
There are some abstractions used that may be seen in the project structure such as:

- Loaders - An abstraction responsible for loading stuff.  
- Sinks - An abstraction responsible for putting stuff somewhere.
- Controller - Where the logic resides.
- Config - Loads and validates configurations.
- Transformations - Responsible for transforming data.

If you...
- want to understand the whole flow of code, `main.py` is your entry point
- want to understand a specific module, check its corresponding unit tests

## Some Intentional Decisions
- The database table has a surrogate key as pkey, as an autoincrement. This is because surrogate keys aren't affected to changes in business/application.
- To simplify things, I wasn't concerned about credentials. To a production system, credentials should be stored in a secure place (e.g. AWS Parameter Store, Vault, etc....)

## Some Points of Improvement
- There's a flattening of json happening on the loader. This can be seen as a break in Single Responsibility. The best way to address this IMO is to turn the flattening into a transformation.
- One of the layers of the image build is always being executed. Is there a way to avoid this?

## Environment
Just for the sake of debugging if fails to run on docker, this is my current environment:
- Docker version 24.0.6, build ed223bc820
- Docker Compose version v2.24.7
- SO:
  - ProductName:		macOS
  - ProductVersion:		13.6.4
  - BuildVersion:		22G513