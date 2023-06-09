import pandas as pd
from datasets import Dataset

df = pd.read_excel('NaverScrapper/result/__crawled_data.xlsx')

df.to_parquet("dataset.parquet", row_group_size=100, engine="pyarrow", index=False)

ds = Dataset.from_parquet("dataset.parquet")
ds.push_to_hub("CertifiedJoon/Korean-Instruction")