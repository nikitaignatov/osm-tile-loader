# Extract map tiles from OSM to sdcard

## Setup the server
Map tiles can be downloaded from https://download.geofabrik.de/ to then be loaded into the container
a more detailed guide can be found here: https://github.com/Overv/openstreetmap-tile-server

In the following example map of Denmark is downloaded and then attached to the docker container.
Script will take some time to first load the maps and then load the docker images.

```
wget https://download.geofabrik.de/europe/denmark-latest.osm.pbf
docker volume create osm-data

docker run \
  -v /home/user/denmark-latest.osm.pbf:/data/region.osm.pbf \
  -v osm-data:/data/database/  overv/openstreetmap-tile-server \
  import

docker run \
 -p 8080:80 \
 -v osm-data:/data/database \
 -d overv/openstreetmap-tile-server \
 run
```

When container is running, navigate to review the maps

http://localhost:8080

The tiles can be loaded via following url

http://localhost:8080/tile/0/0/0.png
