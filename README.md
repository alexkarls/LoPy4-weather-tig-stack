# Instructions

## Issues

**You may encounter a common issue related to Grafana permissions.**

Example issue can be seen below:


*grafana | mkdir: can't create directory '/var/lib/grafana/plugins': Permission denied.*

This issue can be resolved by changing the permissions for the Grafana volume (bind mount). This folder is located at the path *./grafana/volume*. The permission need to be changed to the Grafana user and group.

**Example solution can be seen below:**


*sudo chown -R 472:472 ./volumes/grafana*