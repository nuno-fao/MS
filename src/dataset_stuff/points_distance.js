const fs = require('fs');

fs.readFile("files/step2.json", 'utf8', (err, data) => {
    const distances = {}
    const ps = {}
    if (err) {
        console.error(err);
        return;
    }
    let points = JSON.parse(data)
    let i = 0
    for (const point of points) {
        ps[point[0] + "_" + point[1]] = i
        distances[i] = {}
        i++
    }

    i = 0

    for (const point of points) {
        i++
        let current_point = ps[point[0] + "_" + point[1]]
        for (const op of points.slice(i)) {
            const other_point = ps[op[0] + "_" + op[1]]
            const d = distance(point[0], point[1], op[0], op[1])
            distances[current_point][other_point] = d
            distances[other_point][current_point] = d
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