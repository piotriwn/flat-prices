# Python + Beautfiul Soup + Properties for sale site
This script uses python's Beautiful Soup to extract information from Polish popular site containing properties for sale [Gratka](www.gratka.pl).

The script connects to a number of "subsites" to get data from all the offers. The data is then saved to csv file formatted in the following way:

District | Area | Rooms | Total price | Price per meter square
------------ | ------------- | ------------- | ------------- | -------------
data | data | data | data | data

Modules used:
* bs4
* urllib
* re
* csv

Specifics of the code included as comments in main.py.