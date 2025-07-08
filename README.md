# Web_Scraping
Pipeline ETL de web scraping de datos de contacto respetando normativas eticas y legales. Escalable y rastreable. 

0.1- Los registros fueron brindados a traves de 122 plnillas de excel. Se unificaron los registros por segmentacion de tiempo.
0.2- Se unificaron todos los segmentos de tiempo en un solo df. Paso importante para realizar conclusion analitica. 
1- Se unificaron los nros de teléfonos brindados para comparar con los scrapeados. Sirve ademas para calcular el porcentaje de exito.
2- Se preaparan los registros para scrapear en formato batch de forma paralelizada; optimiza la gran cantidad de registros y los tiempos necesarios del proceso.
3- Scrapeo en formato batch. Por cada batch se prepara 1 fragmento (FRG_1, FRG_2, etc.).
4- Se unifican los telefonos scrapeados de forma exitosa en una df para comparar los con del df "1". 
5- Aquellos con error son unificados en un df para pasar por una segunda capa más rigurosa.
6- Ejecucion de la segunda capa que trabaja a contramano de la primera capa. Cada una capta los registros que no son captados por la otra.
7- Comparacion final de todos los telefonos scrapedos vs los brindados por la empresa.

Informe final realizado en Power BI analizando métricas del funcionamiento del flujo.
