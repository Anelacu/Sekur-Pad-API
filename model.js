var mongoose = require('mongoose')

var logSchema = mongoose.Schema({
  userUuid: {type: String, required: true},
  logUuid: {type: String, required: true},
  timestamp: {type: String, required: true},
  activity: {type: String, required: true}
});

var Log = module.exports = mongoose.model('log', logSchema);

module.exports.get = function(callback, limit) {
  Log.find(callback).limit(limit);
}