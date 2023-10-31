const successResponse = function(res, result, code= 200) {
  return res.status(code).json({ status: true, data: result });
}

const errorResponse = function(res, code, errorMessage) {
  return res.status(code).json({ status: false, error: { message: errorMessage } });
}

module.exports = { successResponse, errorResponse };