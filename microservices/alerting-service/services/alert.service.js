
const nodemailer = require("nodemailer");

const  sendEmail = async (reqBody) => {

    let { from_, to, subject, message } = reqBody;

    let transporter = nodemailer.createTransport({
        service: 'gmail',
        auth: {
            user: 'example@example.com',
            pass: 'ENTER_PASSWORD_HERE'
        }
    })
    let mailOptions = {
        from: from_,
        to: to,
        subject: subject,
        html: message
    }

    transporter.sendMail(mailOptions, function(error, info){
        if (error) {
            console.log(error);
        } else {
            console.log('Info .... ' + info);
            console.log("Email Sent: " + info.response);
        }
    });

}

module.exports = { sendEmail }

