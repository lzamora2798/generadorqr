
from django.shortcuts import  render
from reportlab.lib import utils
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO
import os
import qrcode as qr
from django.conf import settings

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
        print(settings.STATIC_ROOT)
        img.save(settings.STATIC_ROOT+"/image/"+str(RUC)+".png")
    else:
        pass
    print(Nombre)
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
    os.remove(settings.STATIC_ROOT+"/image/"+str(RUC)+".png")
    return response
