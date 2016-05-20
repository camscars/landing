from django.shortcuts import render
from django.core.mail import send_mail
from .forms import SignUpForm, ContactForm
# Create your views here.
def home(request):
	title = 'Join email list'
	form = SignUpForm(request.POST or None)
	if form.is_valid():
		form.save()
	return render(request, 'homepage.html', {'title': title, 'form': form})

def about(request):
	return render(request, "about.html")

def project_list(request):
	return render(request, "project_list.html")

def contact(request):
	title = 'Contact Me'
	form = ContactForm(request.POST or None)
	if form.is_valid():
		form_email = form.cleaned_data.get("email")	
		form_message = form.cleaned_data.get("message")
		form_full_name = form.cleaned_data.get("full_name")
		# print email, message, full_name
		subject = 'Site contact form'
		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email, 'youotheremail@email.com']
		contact_message = "%s: %s via %s"%( 
				form_full_name, 
				form_message, 
				form_email)
		html_message = """<h1>Hi</h1>"""
		send_mail(subject,
				contact_message,
				from_email,
				to_email,
				html_message=html_message,
				fail_silently=True)
	return render(request, "contact.html", {"title": title, "form": form})