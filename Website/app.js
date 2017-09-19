const express = require("express");
const mysql = require("mysql");
const bodyParser = require("body-parser");
const chartjs = require('chart.js');
const path = require("path");

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

app.listen(3000, function(){
  console.log("Server started on port 3000");
});

app.get('/', function(req, res) {
  // fucntions
  function getLabels() {
    var labelArr = "[";
    for (var i = 0; i < 10; i++) {
      if( i != 10 - 1) {
        labelArr += "\"" + i + "\", ";
      }
      else {
        labelArr += "\"" + i + "\"]";
      }
    }
    return labelArr;
  };

  function getData() {
    var dataArr = new Array(10);
    for (var i = 0; i < dataArr.length; i++) {
      dataArr[i] = Math.floor(Math.random() * 100);
    }
    return dataArr;
  };

  var labels = getLabels();
  var filteredData = getData();
  var unfilteredData = getData();

  res.render("index", {
    labels : labels,
    datafil : '[' + filteredData + ']',
    dataunfil : '[' + unfilteredData + ']'
  });
});
