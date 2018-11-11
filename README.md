# Cockroach


Cockroach is a utility for retrieving and sorting historical data from a web archive. Sometimes 
it can help in the pentest of a web application. For example, an older version of a robots.txt 
file may contain entries about interesting directories or documents.

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
 
* **robots**  
Get all robots.txt records for a domain

**-d example.com, --domain example.com** - Domain for which to search  

Historical data range(Default range: all last year):  
**-s yyyymmdd, --startdate yyyymmdd** - Start date in yyyymmdd format. For example 19700130  
**-e yyyymmdd, --enddate yyyymmdd** - End date in yyyymmdd format. For example 19700130

* **range**  
Check available date range in history  

**-d example.com, --domain example.com** - Domain for which to search  

