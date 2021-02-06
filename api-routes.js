let router = require('express').Router();
var logController = require('./log-controller');

router.get('/', function(req, res) {
  res.json({status: 'API is working', message: 'Henlo working'});
});

router.route('/logs').get(logController.index).post(logController.new);

module.exports = router;
