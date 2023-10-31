const alertService = require('../services/alert.service');
const { successResponse, errorResponse } = require('../commons/response.util');

const test = async function(req, res) {
    return successResponse(res, 'test success from alert api');
}
const sendEmail = async function(req, res) {
        let reqBody = req.body;

        let { from_, to, subject, message } = reqBody;

        let emailSent = await alertService.sendEmail(reqBody);

        let resObj = {
            message: 'email sent successfully',
            details: {
                from_,
                to,
                subject,
                message
            }
        };
    return successResponse(res, resObj);
}

module.exports = { sendEmail, test };
