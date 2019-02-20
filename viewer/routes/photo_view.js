var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('photo_view', { title: 'photo_view' });
});

module.exports = router;