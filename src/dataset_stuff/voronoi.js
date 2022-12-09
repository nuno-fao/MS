const {createCanvas} = require("canvas");
const fs = require("fs");

// Dimensions for the image
const width = 1200;
const height = 627;

// Instantiate the canvas object
const canvas = createCanvas(width, height);
const context = canvas.getContext("2d");

// Fill the rectangle with purple
context.fillStyle = "#764abc";
context.fillRect(0, 0, width, height);

// Write the image to file
const buffer = canvas.toBuffer("image/png");