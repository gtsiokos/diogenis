
def handle_uploaded_pdf(pdf):
	path = open('/home/fusion/diogenis/media/anatheseis.pdf', 'wb+')
	for chunk in pdf.chunks():
		path.write(chunk)
		path.close()
