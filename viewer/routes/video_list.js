var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
	var fs = require('fs');
	fs.readdir('.', function(err, files){
    	if (err) throw err;
    	var fileList = files.filter(function(file){
        	return fs.statSync(file).isFile(); //絞り込み
    	})
    	console.log(fileList);
	});
	res.render('video_list', { title: fileList });
});

module.exports = router;