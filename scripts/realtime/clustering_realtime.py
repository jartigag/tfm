#!/usr/bin/env python3
#
#usage: ./clustering_realtime.py /home/javi/clustering/2020-09-22-dataset.csv
#exec time: 7s
#output example:
# $ head 2020-09-22-dataset.labeled.csv
# src_ip,dst_ip,proto,src_port,dst_port,anom_level,threat_level,max_prio,count_events,avg_duration,stdev_duration,cluster
# 10.253.15.238,98,0,4624,3,0.03,0.0,4,13111,184.49,2563.48,1
# 172.24.82.135,293,1,3264,6,0.01,0.0,4,12951,321.74,710.02,0
#$ column -ts, 2020-09-19-dataset.clustresum.csv
#centroids:
#cluster            dst_ip  proto  src_port  dst_port  anom_level  threat_level  max_prio  count_events  avg_duration  stdev_duration
#0                  290.83  0.81   7035.31   4.86      0.08        0.0           3.99      24410.53      99.11         741.55
#1                  92.25   0.1    2051.89   2.25      0.18        0.0           4.0       4840.12       57.37         675.72
#2                  8.18    0.4    387.35    3.0       0.0         0.0           5.0       1045.94       357.9         872.4
#3                  21.0    2.0    980.0     1051.0    0.0         0.0           5.0       2319.0        48.32         102.88
#4                  37.71   0.26   613.76    2.15      0.1         0.0           4.5       3148.45       2587.11       10194.99
#size of clusters:
#cluster            size(%)
#0                  33.15
#1                  52.19
#2                  12.56
#3                  0.02
#4                  2.08

import sys
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

df_data = pd.read_csv( open(sys.argv[1]) )
scaler = StandardScaler()
X = scaler.fit_transform(df_data.loc[:,df_data.columns!="src_ip"])

algo = KMeans(n_clusters = 5)
clusters = algo.fit_predict(X)

centroids = scaler.inverse_transform(algo.cluster_centers_)
df_centroids = pd.DataFrame(centroids, columns=df_data.columns.drop('src_ip'))

df_data['cluster'] = pd.Series(algo.labels_)

# {
# print to csv:
df_data.to_csv(f"{sys.argv[1].strip('csv')}labeled.csv", index=False)

clustresum = f"{sys.argv[1].strip('csv')}clustresum.csv"
with open(clustresum, mode='a') as clustresumf:
    print("centroids:", file=clustresumf)
    df_centroids.round(2).to_csv(clustresumf, index_label="cluster")
    print("size of clusters:", file=clustresumf)
    df_data.groupby('cluster').size().to_frame('size(%)').transform( lambda x: 100*x/sum(x) ).round(2).to_csv(clustresumf, index_label="cluster")
# }