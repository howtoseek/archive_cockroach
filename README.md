# Cockroach


Cockroach is a utility for retrieving and sorting historical data from a web archive. Sometimes 
it can help in the pentest of a web application. For example, an older version of a robots.txt 
file may contain entries about interesting directories or documents.  

Еhe following functions are now available:  
* **robots** - Get all unique records of robots.txt files for a specified period of time  
* **range** - Check available date range in history for a domain  

## Install

#### Prerequisites  
`python >=3.5`

#### Install in Python Virtual Environments  

* Download  
`git clone https://github.com/howtoseek/archive_cockroach.git`  
`cd archive_cockroach`  
* Creating Virtual Environments  
`python3.5 -m venv env`  
* Activate  
`source env/bin/activate`  
* install requirements  
`pip3.5 install -r requirements.txt`  

#### Normal installation

_Requires root privileges to install dependencies_  

* install requirements  
`pip3.5 install -r requirements.txt`

## Usage

The cockroach has several subcommands for different actions. Each subcommand has its own set of options.
Type `cockroach.py action_command -h` to view additional options.  
 
* **robots** - Get all unique records of robots.txt files for a specified period of time  

Options:  
*-d example.com, --domain example.com* - Domain for which to search  

Historical data range(Default range: all last year):  
*-s yyyymmdd, --startdate yyyymmdd* - Start date in yyyymmdd format. For example 19700130  
*-e yyyymmdd, --enddate yyyymmdd* - End date in yyyymmdd format. For example 19700130

* **range** - Check available date range in history for a domain  

Options:  
*-d example.com, --domain example.com* - Domain for which to search  

## Example  

* Check the date range for available data in the archive.  

`$ ./cockroach.py range -d example.com`  

Output:  
_For the domain example.com available data for the period:   
Earliest date: 20020120142510  
Latest date: 20181113123833_  

* Get all the unique robots.txt files records for the period from 01/01/2017 to 31/12/2017.  

`$ ./cockroach.py robots -d example.com -s 20170101 -e 20171231`  

* Or get the unique robots.txt files records from 01/01/2018 to the current day.  

`$ ./cockroach.py robots -d example.com -s 20180101`

* Or get the unique robots.txt files records for the last 365 days  

`$ ./cockroach.py robots -d example.com`  


