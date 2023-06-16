from django.shortcuts import render,redirect
from store.forms import ContactForm

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data or perform other actions
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            message = form.cleaned_data['message']
            # Access other form fields
            
            # Redirect to a success page or perform other actions
            return redirect('contact_success')
    else:
        form = ContactForm()
        
    return render(request, 'contact.html', {'form': form})