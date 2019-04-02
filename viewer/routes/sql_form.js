var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
	var mysql = require('mysql');
	var result = [];
	global.result = [];
	var connection = mysql.createConnection({
		host	: 'localhost',
		user	: 'pi',
		password: 'password',
		database: 'database'
	});
	connection.connect(function(err){
		if(err){
			console.error('error connecting: ' + err.stack);
			return;
		}
		console.log('success');
	});

	var rendCallback = function(result_true){
		console.log('render');
		connection.end();
		console.log(result_true);
		res.render('sql_form',{ title : result_true });
	}
	function testsql(callback){
		console.log('querry');
		connection.query('select * from sensor;',function(err,rows,fields){
			if (err){
				console.log('err: ' + err);
			}
			var res = [];
			for(i=0,j=rows.length;i<j;i++){
				res.push(rows[i].date);
				res.push(rows[i].time);
				res.push(rows[i].place);
			}

			var result = JSON.stringify(res);
			callback(result);
		});
	};
	testsql(rendCallback);
});

module.exports = router;
