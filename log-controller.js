let Log = require('./model')

// Handle index actions
exports.index = function(req, res) {
  Log.get(function(err, logs) {
    if (err) {
      res.json({
        status: 'error',
        message: err,
      });
    }
    res.json({
      status: 'success',
      message: 'Logs retrieved successfully',
      data: logs
    });
  });
};

// Handle create log actions
exports.new = function(req, res) {
  var log = new Log();
  log.userUuid = req.body.userUuid;
  log.timestamp = req.body.timestamp;
  log.activity = req.body.activity;
  log.save(function(err) {
    res.json({message: 'New log created!', data: log});
  });
};