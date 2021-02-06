let express = require('express')
let bodyParser = require('body-parser');
const mongoose = require('mongoose')
const cors = require('cors');

let app = express();
const port = process.env.PORT || 8080;
const uri = process.env.URI;

app.use(cors());

mongoose.connect(uri, {useNewUrlParser: true, useUnifiedTopology: true})
    .then(() => {
        console.log('MongoDB Connected…')
    })
    .catch(err => console.log(err));

app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());

app.get('/', (req, res) => res.send('Henlo'));

app.listen(port, function () {
    console.log('Henlo from ' + port);
});

let apiRoutes = require('./api-routes')
app.use('/api', apiRoutes)