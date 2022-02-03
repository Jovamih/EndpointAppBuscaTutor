const nodemailer = require("nodemailer");
const mailCtrller = {};

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

mailCtrller.enviarMensaje = async (req, res) => {
    var correo_destino = 'gaa';
    console.log(correo_destino);
    console.log(req.params.correo_destino);
    //console.log(correo_destino);
    //Envío del correo
    await transporter.sendMail({
        from: '"Confirmación de pago exitosa" <soporte.buscatututor@gmail.com>', // sender address
        to: correo_destino, // list of receivers
        subject: "Validación de suscripción", // Subject line
        html: `¡Hola!<br>
        Estamos muy felices de poder contar contigo como uno de nuestros tutores, 
        el monto por la suscripción fue de $ 5.99, cuando finalice tu
        suscripción se te volverá a solicitar otro pago, para cualquier consulta
        contactarnos a nuestro correo de soporte <a>soporte.buscatututor@gmail.com</a><br>
        ¡Gracias por confiar en nosotros, saludos!`
      });
    res.json({message: "envío exitoso"});
};

module.exports = mailCtrller;