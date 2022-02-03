const { Router } = require('express');
const router = Router();
const {enviarMensaje} =require('../controllers/mail.controller');

//http://localhost:4000/api/send_mail
router.route('/')
    .post(enviarMensaje);

module.exports = router;