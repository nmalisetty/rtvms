const express = require('express');
const router = express.Router();

const mainController = require('../controller/main.controller');

const multer = require('multer');
const upload = multer().single('file');

router.get('/test', mainController.test);

router.post('/stream/process/data', upload, mainController.processData);

router.post('/alerting', mainController.alerting);

router.post('/notification', mainController.notification);

module.exports = router;
