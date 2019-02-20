var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('sql_view', { title: 'sql_view' });
});

module.exports = router;