let express = require('express')

let app = express();
var port = 8080;

app.get('/', (req, res) => res.send('Henlo'));

app.listen(port, function() {
    console.log("Henlo from " + port);
});
