const streamingData = async (reqBody) => {
    console.log('reqBody .... ' + JSON.stringify(reqBody));
}

const alerting = async (reqBody) => {
    console.log('decision to send alerts here');
    console.log('reqBody .... ' + JSON.stringify(reqBody));
}

const notification = async (reqBody) => {
    console.log('decision to handle beacon/acknowledgement here');
    console.log('reqBody .... ' + JSON.stringify(reqBody));
}

module.exports = { streamingData, alerting, notification }


