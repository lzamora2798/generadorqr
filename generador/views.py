
from django.shortcuts import  render
from reportlab.lib import utils
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO
import os
import qrcode as qr
RUC = None
Nombre = None
dato_url = None
img =None

def home(request):
    global RUC
    global Nombre
    global dato_url
    global img
    if request.method == 'POST':
        RUC = request.POST['RUC']
        Nombre = request.POST['Nombre']
        img = qr.make(RUC+Nombre)
        #img.save("static/image/"+str(RUC)+".png")
    else:
        pass
    return render(request, "home.html", {'RUC':RUC,'Nombre':Nombre})

def reporte(request):
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename=codigoQR.pdf'
    buffer = BytesIO()
    c = canvas.Canvas(buffer,pagesize=A4)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50,750,"Ruc:")
    c.setFont("Helvetica", 24)
    c.drawString(110, 750,str(RUC))
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, 700, "Nombre :")
    c.setFont("Helvetica", 24)
    c.drawString(160, 700, str(Nombre))
    c.drawImage(utils.ImageReader(img._img), 50, 150, 500, 500, preserveAspectRatio=True)
    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    os.remove("static/image/"+str(RUC)+".png")
    #{% with '/image/'|add:RUC|add:'.png' as image_path %}
    return response

"""
<div class="contact1-pic" data-tilt>
				{% if RUC %}
                    {% with '/image/wtf.png' as image_path %}
                    <img  alt="No Image" src="{% static image_path %}" />
                    {% endwith %}
                {% else %}
                <h1>Ingrese informacion Oficial</h1>
                {% endif %}
				<a href="/reporte" class="contact1-form-btn" style="text-decoration: none;">
                	Generar PDF
            	</a>
			</div>
"""