#/bin/bash
docker pull mediagis/nominatim
docker run -it --shm-size=4g \
  -e PBF_URL=https://download.geofabrik.de/asia/china-latest.osm.pbf \
  -e REPLICATION_URL=https://download.geofabrik.de/asia/china-updates/ \
  -v nominatim-data:/var/lib/postgresql/14/main \
  -v /osm-maps/data:/nominatim/data \
  -p 8111:8080 \
  --name nominatim \
  mediagis/nominatim:4.2
