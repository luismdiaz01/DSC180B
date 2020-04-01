FROM ucsdets/scipy-ml-notebook

USER root

RUN conda install --quiet --yes geopandas
