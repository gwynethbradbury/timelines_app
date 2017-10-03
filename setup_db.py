import flasktasks
from flasktasks.database.seed import run_seed

if __name__ == '__main__':
    flasktasks.db.create_all()
    run_seed()

# SQL:
# create database taskmanagement;

# Python:
# python setup_db.py

# SQL:
# use taskmanagement
# insert into tag (name,color) values ('DBAS',3);
# insert into tag (name,color) values ('Online Learning',2);