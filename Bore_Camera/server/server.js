const express = require('express')
const bodyParser = require('body-parser')
const app = express()
const port = 3000
const fs = require('fs');
var configData = require("./cv_config/cv_config.json");
// Set up middlewares 
app.use(bodyParser.json())
app.use(express.static('public/www'));
// Get handlers for getting local config file 
app.get('/configData', (req, res) => {
  const config = configData;
  res.send(config);
})

app.post('/configData', (req, res) => {
  console.log(req.body);
  const inputConfig = req.body.configData;
  console.log(inputConfig);
  fs.writeFile('cv_config/cv_config.json', JSON.stringify(inputConfig), (err) => {
     if (err) {
         console.log(err);
         res.send(err);
     }
     else {
         configData = inputConfig;
         console.log(configData);
         console.log("Written config");
         res.send({status: "written config"});
     }
  });
  
})
app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
});