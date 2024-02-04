#!/bin/bash

result=$(sqlite3 weather_backup.db "select * from weather where id>2000;")

echo "$result" > temp.sql
