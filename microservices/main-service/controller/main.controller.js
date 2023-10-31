
const mainService = require('../services/main.service');
const { successResponse, errorResponse } = require('../commons/response.util');

const test = async function(req, res) {
    return successResponse(res, 'test success from main service api');
}

const streamingData = async function(req, res) {
    const reqBody = JSON.parse(req.file.buffer.toString());

    console.log('reqBody', reqBody);

    let resObj = {
        message: 'data streamed successfully',
        details: {
            reqBody
        }
    };

    return successResponse(res, resObj);
}

const alerting = async function(req, res) {
    let reqBody = req.body;

    let { type, source, id, data } = reqBody;

    let alert = await mainService.alerting(reqBody);

    let resObj = {
        message: 'alert sent successfully',
        details: {
            type,
            source,
            id,
            data
        }
    };

    return successResponse(res, resObj);
}

const notification = async function(req, res) {
    let reqBody = req.body;

    let { type, source, id, data } = reqBody;

    let notification = await mainService.notification(reqBody);

    let resObj = {
        message: 'notification sent successfully',
        details: {
            type,
            source,
            id,
            data
        }
    };

    return successResponse(res, resObj);
}

module.exports = { processData: streamingData, alerting, notification, test };
