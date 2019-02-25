var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
	var fs = require('fs');
	var mysql  = require('mysql');
	var result = [];
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
	var filecallback = function(sql_result){
		fs.readdir('./public/movie', function(err, files){
    		if (err) throw err;
    		var fileList = files.filter(function(file){
    			try{
        			return fs.statSync("./public/movie/"+file).isFile(); //絞り込み
        		}catch{
        			return false;
        		}
    		});
    		console.log(fileList);
			var json_text = JSON.stringify(fileList);
			res.render('index',{mov_lis : json_text,sql_res : sql_result});
		});
	};

	var rendCallback = function(result_true){
		console.log('render');
		connection.end();
		//console.log(result_true);
		filecallback(result_true);
		//res.render('sql_form',{ title : result_true });
	};
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