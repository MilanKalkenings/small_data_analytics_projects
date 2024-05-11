# small_data_analytics_projects
various data science notebooks 


# edgecase sampling
- selecting top k most differenct vectors often fails at finding a versatile set of edgecases
- instead: iteratively select most distant data point and discard vectors that point to similar direction from future considerations
- method can be repeated, without reconsidering sampled data points to sample data points after all data points are discarded
- generalizable to high dimensional space

 ![sampling](https://github.com/MilanKalkenings/small_data_analytics_projects/assets/70267800/a662507a-7297-4faf-892c-3f43db3f2cfb)


# wikidata names
- fetch names from wikidata (https://www.wikidata.org/wiki/Wikidata:Main_Page)
- split them into clean forenames and last names
- clustering forename embeddings allows to infer genders

![name_clusters](https://github.com/MilanKalkenings/small_data_analytics_projects/assets/70267800/6bac44a6-42d0-4d74-bddb-71c068d650ef)


# apriori
- one of my first projects ever 
- naive implementation of apriori for frequent set mining on health data

<img width="359" alt="apriori" src="https://github.com/MilanKalkenings/small_data_analytics_projects/assets/70267800/e25186f6-b721-4a3c-8783-29ed0013db0c">

# data cleaning
- one of my first projects ever
- experiments with various data cleaning methods 

![__results___21_0](https://github.com/MilanKalkenings/small_data_analytics_projects/assets/70267800/2c4f0a65-9502-44b9-975d-97f1a6218099)

# feature engineering
- one of my first projects ever 
- experiments with various feature engineering methods 

![__results___37_0](https://github.com/MilanKalkenings/small_data_analytics_projects/assets/70267800/fe5443b9-5d33-4a61-9c3a-0b95afc4a8b3)

# pca
- one of my first projects ever
- simple implementation of principal component analysis for dimensionality reduction

![pca](https://github.com/MilanKalkenings/small_data_analytics_projects/assets/70267800/5021b150-e06b-4c93-af76-f68016b2739f)


# zip code area distances
- calculate distance (km) between zip code area centers
- dataset
  - downloaded at: https://public.opendatasoft.com/explore/dataset/georef-germany-postleitzahl/export/
  - made available by: https://www.suche-postleitzahl.org/
  - based on data from: https://www.openstreetmap.org/#map=4/48.25/11.29
  - provided under Open Data Commons Open Database License (ODbL) v1.0 (https://opendatacommons.org/licenses/odbl/1-0/)

![zip](https://github.com/MilanKalkenings/small_data_analytics_projects/assets/70267800/534b15d3-e289-4d2d-ba2f-c6f71f6ee7ec)
