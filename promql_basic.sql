up{job="node1_rhel10"}

up{instance="13.201.173.103:9113"}

up{company="LW",dc="IN"}

up{company="LW",dc!="IN"}

node_cpu_seconds_total{dc="IN",instance="13.203.23.152:9100",cpu="1",mode="iowait"}


node_cpu_seconds_total{dc="IN",instance="13.203.23.152:9100",cpu="1",mode=~"idle|iowait"}

rate( node_cpu_seconds_total{app="db", company="LW", cpu="0", dc="IN", instance="13.203.23.152:9100", job="node1_rhel10", mode="idle"}[5m] )


sum(node_filesystem_size_bytes)

node_memory_MemFree_bytes + node_memory_Cached_bytes

( node_memory_MemFree_bytes + node_memory_Cached_bytes) / (1024 * 1024)

node_filesystem_avail_bytes > 5*1024*1024*1024


go_goroutines > bool go_threads

up{job="prometheus"} or up{job=~"node1.*"}

time() - prometheus_tsdb_lowest_timestamp_seconds






