var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: "Spoingus' Emporium" });
});

router.get('/login', function(req, res, next){
  res.render('login')
});

router.get('/products', function(req, res, next){
  res.render('products')
});

router.get('/prod/:productID/', function(req, res, next){
  console.log(req.params);
  res.render('products')
});

module.exports = router;
