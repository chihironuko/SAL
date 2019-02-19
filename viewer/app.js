var express = require("express");
var app = express();

// テンプレートエンジンの指定
app.set("view engine", "ejs");
app.use(express.static('public'));
/*
app.get("/", function (req, res){
	res.render('./index/main.html');
});
*/

app.get("/video_watch", function (req, res) {
    res.render('./video.ejs', { title: 'test' });
	var fs = require('fs');
	fs.readdir('.', function(err, files){
		if (err) throw err;
    	var fileList = [];
    	files.filter(function(file){
       		return fs.statSync(file).isFile(); //絞り込み
    	}).forEach(function (file) {
       		fileList.push(file);
    	});
    	console.log(fileList);
	});
});

app.listen(3000);