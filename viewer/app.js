var createError = require('http-errors');
var express = require("express");
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');

//index page
var indexRouter = require('./routes/index');
//dust
var usersRouter = require('./routes/users');
//video main page
var videoRouter = require('./routes/video');
//sql form page
var sqlRouter = require('./routes/sql');
//photo main page
var photoRouter = require('./routes/photo');

var app = express();

app.set('views', path.join(__dirname,'views'));
// テンプレートエンジンの指定
app.set('view engine', 'ejs');
app.use(express.static('public'));


app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);
app.use('/users', usersRouter);
app.use('/video', videoRouter);
app.use('/sql', sqlRouter);
app.use('/photo', photoRouter);

app.use(function(req,res,next){
	next(createError(404));
});

app.use(function(err, req, res, next){
	res.locals.message = err.message;
	res.locals.error=req.app.get('env') === 'development' ? err : {};

	res.status(err.status || 500);
	res.render('error');
});









/*
app.get('/', function (req, res){
	res.send('Hello');
});


app.get("/video_list", function (req, res) {
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

*/

module.exports = app;