#!/bin/sh
sqlite3 -header fuelprices.db 'select * from prices order by day desc, fuel asc'
