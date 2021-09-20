# import os
# import dotenv
import sqlalchemy as alch


# dotenv.load_dotenv()

# passw = os.getenv("pass_sql")
passw = "admin"
dbName="political_debates"
connectionData=f"mysql+pymysql://root:{passw}@localhost/{dbName}"
engine = alch.create_engine(connectionData)
