var createError = require('http-errors');
var express = require("express");
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var session = require('express-session');

var session_opt = {
	secret: 'keyboard cat',
	resave: false,
	saveUninitialized: false,
	cookie: {maxAge: 60 * 60 * 1000}
};


//index page
var indexRouter = require('./routes/index');
//dust
var usersRouter = require('./routes/users');
//video main page
var videoListRouter = require('./routes/video_list');
//sql form page
var sqlFormRouter = require('./routes/sql_form');
//photo main page
var photoListRouter = require('./routes/photo_list');
//video main page
var videoViewRouter = require('./routes/video_view');
//sql form page
var sqlViewRouter = require('./routes/sql_view');
//photo main page
var photoViewRouter = require('./routes/photo_view');



var app = express();
app.use(express.static('public'));

app.set('views', path.join(__dirname,'views'));
// テンプレートエンジンの指定
app.set('view engine', 'ejs');



var ajax = require('./routes/ajax');
app.use('/ajax', ajax);
app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
app.use(session(session_opt));

app.use('/', indexRouter);
app.use('/users', usersRouter);
app.use('/video_list', videoListRouter);
app.use('/sql_form', sqlFormRouter);
app.use('/photo_list', photoListRouter);
app.use('/video_view', videoViewRouter);
app.use('/sql_view', sqlViewRouter);
app.use('/photo_view', photoViewRouter);

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