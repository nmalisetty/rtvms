const express = require('express');
const router = express.Router();

const alertController = require('../controller/alert.controller');

//test get api
router.get('/test', alertController.test);

router.post('/email', alertController.sendEmail);


module.exports = router;
