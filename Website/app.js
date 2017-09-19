const express = require("express");
const mysql = require("mysql");
const bodyParser = require("body-parser");
const chartjs = require('chart.js');
const path = require("path");
const sqlite3 = require('sqlite3').verbose();

const app = express();

/* Middlewear */

// Embedded javascript view engine
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

// Body parser middlewear
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));

// Public folder middlewear
app.use(express.static(path.join(__dirname, "public")));
var labelArr = ""
var unfiltered = []
var filtered = []
var db;

function connctdb(req, res, next) {
  db = new sqlite3.Database('db/data.db', (err) => {
    if (err) {
      console.error(err.message);
    }
    console.log('Connected to the database.');
  });
  next();
}

function getdata(req, res, next) {
  db.serialize(function() {

    db.each("SELECT seconds, unfiltered, filtered FROM co2_data", function(err, row){

      if (err)
        console.log(err);
      else {
        labelArr += "\"" + row.seconds + "\" ";
        unfiltered.push(row.unfiltered)
        filtered.push(row.filtered)
      }
    })
    db.close();
  })

  next();
}

app.get('/', connctdb, getdata, function(req, res) {
  // // fucntions
  // function getLabels() {
  //   var labelArr = "[";
  //   for (var i = 0; i < 10; i++) {
  //     if( i != 10 - 1) {
  //       labelArr += "\"" + i + "\", ";
  //     }
  //     else {
  //       labelArr += "\"" + i + "\"]";
  //     }
  //   }
  //   return labelArr;
  // };
  //
  // function getData() {
  //   var dataArr = new Array(10);
  //   for (var i = 0; i < dataArr.length; i++) {
  //     dataArr[i] = Math.floor(Math.random() * 100);
  //   }
  //   return dataArr;
  // };
    res.render("index", {
      labels : '[' + labelArr.substr(0, labelArr.length - 1) + ']',
      datafil : '[' + filtered + ']',
      dataunfil : '[' + unfiltered + ']'
    });
});



app.listen(3000, function(){
  console.log("Server started on port 3000");
});
