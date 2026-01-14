from ETL.extract import extract
from ETL.transform import transform
from ETL.load import load

if __name__ == "__main__":
    extract(1) # para: no_movies_to_get_para:int = 1
    transform()
    load()



