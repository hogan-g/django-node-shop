var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: "Spoingus' Emporium" });
});

router.get('/login', function(req, res, next){
  res.render('login')
});

router.get('/logout', function(req, res, next){
  res.render('logout')
});

router.get('/basket', function(req, res, next){
  res.render('basket')
});

router.get('/order', function(req, res, next){
  res.render('order')
});

router.get('/productindividual', function(req, res, next){
  res.render('productindividual')
});

router.get('/register', function(req, res, next){
  res.render('register')
});

router.get('/prev_orders', function(req, res, next){
  res.render('prevorders')
});

module.exports = router;
