const fs = require('fs');
fs.readFile("files/step2.json", 'utf8', (err, data) => {
    const distances = {}
    if (err) {
        console.error(err);
        return;
    }
    let points = JSON.parse(data)

    for (const p in points) {
        distances[p] = {}
    }


    for (const p in points) {
        let point = points[p]
        for (const op in points) {
            if (p !== op) {
                const d = distance(point[0], point[1], points[op][0], points[op][1])
                distances[p][op] = d
                distances[op][p] = d
            }
        }
    }

    fs.writeFile("files/step3.json", JSON.stringify(distances), 'utf8', (err) => {
        if (err) {
            console.error(err);
            return;
        }
    });
});

function distance(lat1, lon1, lat2, lon2, unit = "K") {
    if ((lat1 === lat2) && (lon1 === lon2)) {
        return 0;
    } else {
        const radlat1 = Math.PI * lat1 / 180;
        const radlat2 = Math.PI * lat2 / 180;
        const theta = lon1 - lon2;
        const radtheta = Math.PI * theta / 180;
        let dist = Math.sin(radlat1) * Math.sin(radlat2) + Math.cos(radlat1) * Math.cos(radlat2) * Math.cos(radtheta);
        if (dist > 1) {
            dist = 1;
        }
        dist = Math.acos(dist);
        dist = dist * 180 / Math.PI;
        dist = dist * 60 * 1.1515;
        if (unit === "K") {
            dist = dist * 1.609344
        }
        if (unit === "N") {
            dist = dist * 0.8684
        }
        return dist;
    }
}