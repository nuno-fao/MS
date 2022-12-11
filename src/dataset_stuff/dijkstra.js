const readlines = require('n-readlines');

class D_Node {
    get lat() {
        return this._lat;
    }

    set lat(value) {
        this._lat = value;
    }

    get lon() {
        return this._lon;
    }

    set lon(value) {
        this._lon = value;
    }

    get id() {
        return this._id;
    }

    set id(value) {
        this._id = value;
    }

    constructor(lat, lon, id) {
        this._lat = lat;
        this._lon = lon;
        this._id = id;
        this._accumulated_distance = 10000000000000.0
    }

}

const closestPoint = (lat, lon, nodes) => {
    let dist = 100000000000000
    let node
    for (const key in nodes) {
        console.log(nodes[key][0], nodes[key][1], lat, lon)
        let local_dist = distance(nodes[key][0], nodes[key][1], lat, lon)
        if (local_dist < dist) {
            node = key
            dist = local_dist
        }
    }
    console.log(dist, node)
}
const dijkstra = (originPoint, targetPoints, edges, nodes) => {
    const visited = {}
    const explored = {}
    closestPoint(originPoint[0], originPoint[1], nodes)
}

const nodes = {}
const edges = {}

let next;

const nodes_liner = new readlines("files/nodes.csv");
nodes_liner.next()
while (next = nodes_liner.next()) {
    const node = next.toString().split(",")
    nodes[node[4]] = [node[0], node[1]]
    edges[node[4]] = {}
}


const edges_liner = new readlines("files/edges.csv");
edges_liner.next()
while (next = edges_liner.next()) {
    const node = next.toString().split(",")
    edges[node[0]][node[1]] = node[2]
}

dijkstra([-22.861678700000002 - 42.9950595], [], edges, nodes)

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