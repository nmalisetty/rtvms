const express = require('express');
const app = express();
const cors = require('cors');
require('dotenv').config();
const port = process.env.SERVER_PORT || 4000;
const routes = require('./routes/alert.route');
const bodyParser = require('body-parser');

app.use(bodyParser.json());
app.use(cors());

app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  res.header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE");
  next();
});

app.use('/alert', routes);

app.listen(port, () => {
  console.info(`Server started on port ${port}`);
});

module.exports = app;