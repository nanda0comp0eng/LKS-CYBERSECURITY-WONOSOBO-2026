#!/bin/sh

echo "Checking database initialization..."
node init-db.js

echo "Starting NotesVault..."
exec node app.js