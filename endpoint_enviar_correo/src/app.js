const express = require('express');
const cors = require('cors');
const app = express();
const nodemailer = require("nodemailer");

transporter = nodemailer.createTransport({
    host: "smtp.gmail.com",
    port: 465,
    secure: true, // true for 465, false for other ports
    auth: {
    user: 'soporte.buscatututor@gmail.com', // generated ethereal user
    pass: 'lrfuuuhfihpcisga', // generated ethereal password
    },
});
transporter.verify().then( () =>{
});

//Settings
app.set('port', process.env.PORT || 4000);

//Middleware
app.use(cors());
app.use(express.json());

app.use('/api/send_mail', require('./routes/mail'));

app.post('/api/enviar/:correo_destino', async function(req, res){
    var correo_destinatario = req.params.correo_destino;
    console.log(correo_destinatario);
    console.log(req.params.correo_destino);
    //console.log(correo_destino);
    //Envío del correo
    await transporter.sendMail({
        from: '"Confirmación de pago exitosa" <soporte.buscatututor@gmail.com>', // sender address
        to: correo_destinatario, // list of receivers
        subject: "Validación de suscripción", // Subject line
        html: `¡Hola!<br>
        Estamos muy felices de poder contar contigo como uno de nuestros tutores, 
        el monto por la suscripción fue de $ 5.99, cuando finalice tu
        suscripción se te volverá a solicitar otro pago, para cualquier consulta
        contactarnos a nuestro correo de soporte <a>soporte.buscatututor@gmail.com</a><br>
        ¡Gracias por confiar en nosotros, saludos!`
      });
    res.json({message: "envío exitoso"});
});

module.exports = app;