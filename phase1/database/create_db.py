from phase1.database import engine

from models import Base

# Create database
print("Creating database ...")
Base.metadata.create_all(engine)
print("Database created successfully ...")