var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
	var mysql      = require('mysql');
	var connection = mysql.createConnection({
		host     : '192.168.100.',
		user     : 'me',
		password : 'secret'
	});
	var test = connection.query('SELECT * FROM `boso` ', function (error, results, fields) {
	});

	res.render('sql_form', { title: 'Express' });
});

module.exports = router;