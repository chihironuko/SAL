var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
	var mysql      = require('mysql');
	var result = [];
	var url = require('url');
	global.result = [];
	/*var connection = mysql.createConnection({
		host     : '192.168.100.7',
		user     : 'home',
		password : 'arvensis_11',
		database : 'boso'
	});*/
	var connection = mysql.createConnection({
		host     : '172.16.162.159',
		user     : 'other',
		password : 'jacx0809mmhsmc',
		database : 'boso'
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
		res.render('sql_view',{ title : result_true });
	}
	function testsql(callback){
		var urlParam = req.url.split('?')[1];
		console.log(urlParam);
		connection.query('select * from sensor where date = ?;',[urlParam],function(err,rows,fields){
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
			/*
			console.log('date: ' + rows[0].date);
			console.log('time: ' + rows[0].time);
			console.log('place: ' + rows[0].place);
			*/
			//return json_txt;
			//res.render('sql_form',{ title : json_txt});
			callback(result);
		});
	};
	testsql(rendCallback);
	//res.render('sql_form',{ title: result });
	//res.render('sql_form', { title: 'Express' });
});

module.exports = router;
