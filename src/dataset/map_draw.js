const {createCanvas} = require("canvas");
const fs = require("fs");

fs.readFile("files/step2.json", 'utf8', (err, data) => {

    const points = JSON.parse(data)

    let leftPoint = [1000, -1000]
    let rightPoint = [-1000, 1000]

    for (let p in points) {
        const point = points[p]
        if (point[0] > leftPoint[1]) {
            leftPoint[1] = point[0]
        }
        if (point[0] < rightPoint[1]) {
            rightPoint[1] = point[0]
        }
        if (point[1] < leftPoint[0]) {
            leftPoint[0] = point[1]
        }
        if (point[1] > rightPoint[0]) {
            rightPoint[0] = point[1]
        }
    }

    const ratio = (rightPoint[0] - leftPoint[0]) / (leftPoint[1] - rightPoint[1])
    console.log(ratio)

    const width = 1200;
    const height = width / ratio;

    // Instantiate the canvas object
    const canvas = createCanvas(width, height);
    const context = canvas.getContext("2d");

    context.fillStyle = "#ffffff";
    context.fillRect(0, 0, width, height);

    context.fillStyle = "#000000";


    for (const p in points) {
        const point = points[p]
        console.log(point)

        context.fillRect(width - width * getR(point[1], rightPoint[0], leftPoint[0]), height - height * getR(point[0], rightPoint[1], leftPoint[1]), 10, 10);
    }

    console.log("\n")
    fs.readFile("files/centroids.json", 'utf8', (err, data) => {
        const points = JSON.parse(data)

        context.fillStyle = "#ff0000";

        for (const p in points) {
            const point = points[p]
            console.log(point)
            context.fillRect(width - width * getR(point[1], rightPoint[0], leftPoint[0]), height - height * getR(point[0], rightPoint[1], leftPoint[1]), 20, 20);
        }

        const buffer = canvas.toBuffer("image/png");

        fs.createWriteStream("./files/points.png").write(buffer);
    })
})

const getR = (v, s, b) => {
    // v = Math.abs(v)
    // b = Math.abs(b)
    // s = Math.abs(s)
    return (v - s) / (b - s)
} 
