var express = require('express');
var router = express.Router();

var data = [];

router.get('/',(req,res,next) => {
	var n = req.query.id;
	res.json(data[n]);
});

module.exports = router;