# Create your views here.
from django.http import Http404, HttpResponse, HttpResponseRedirect
from library.models import Books, Students, BookIssued
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404, redirect
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from library.forms import AddBookForm, AddStudentForm
def index(request):
	if request.user.is_authenticated():
		list_of_books = Books.objects.all()
		return render_to_response('library/index.html', {'list_of_books' : list_of_books}, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/login/')

def mydetails(request):
	if request.user.is_authenticated():
		user = request.user
		try:
			sid = request.POST.get('sid',0 )
			s = Students.objects.get(s_id=sid)
			i = BookIssued.objects.filter(s_id__s_id = sid)
			return render_to_response('library/mydetails.html', {'student':s, 'books':i, 'user':user}, context_instance=RequestContext(request))	
		except ObjectDoesNotExist:
			return render_to_response('library/mydetails.html', {'user':user} , context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/login/')

def returnbook(request):
	if request.user.is_authenticated():
		user = request.user
		s_id = request.POST['s_id']
		sid = Students.objects.get(name=s_id)
		b_id = request.POST['b_id']
		b_id = Books.objects.get(book_name=b_id)
		b_id = BookIssued.objects.get(b_id=b_id, s_id=sid)
		book = b_id.b_id
		book.count += 1
		book.save()
	
		b_id.delete()
		
		return render_to_response('library/confirmreturn.html', {'book':book,'student':sid, 'user':user})
	else:
		return HttpResponseRedirect('/login/')


def issuebook(request, bb_id):
	if request.user.is_authenticated():
		b = Books.objects.get(book_id = bb_id)
		return render_to_response('library/issue.html', {'issue': b}, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/login/')

def confirmation(request, b_id):
	if request.user.is_authenticated():
		user = request.user
		b = Books.objects.get(book_id = b_id)
		error_msg =""
		error_flag = 0
		try:
			sid = request.POST['ssid']
			s = Students.objects.get(s_id=sid)
			try:
				alreadyIssue = BookIssued.objects.get(b_id=b, s_id=s)
				error_msg = "Sorry !!! You already have this book."
				error_flag = 1
				return render_to_response('library/confirm.html',{'book':b, 'student':s, 'msg':error_msg, 'flag':error_flag})
			except ObjectDoesNotExist:	
				b.count -= 1
				b.save()
				c = BookIssued(b_id = b, s_id = s )
				c.save()
		except ObjectDoesNotExist:
			error_msg = "Sorry!!! Incorrect Entry in ID field"
			error_flag = 1
			return render_to_response('library/confirm.html',{'book':b, 'msg':error_msg, 'flag':error_flag, 'user':user})

		return render_to_response('library/confirm.html', {'book':b, 'student':s, 'msg':error_msg, 'flag':error_flag,'user':user})
	else:
		return HttpResponseRedirect('/login/')
def userlogin(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/library/')
	return render_to_response('library/login.html', context_instance=RequestContext(request))

def userauth(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request,user)
				user_id = User.objects.get(username= username).id
				request.session['user_id'] = user_id
				user = User.objects.get(username=username)
				return redirect('/library/',user)
			else:
				error_msg = "Sorry!!! Your Account is Currently Disabled"
				return render_to_response('library/error.html', {'error_msg':error_msg})
		else:
			error_msg = "Sorry!!! Invalid username or password"
			return render_to_response('library/error.html', {'error_msg':error_msg})


def userlogout(request):
	logout(request)
	return render_to_response('library/login.html', context_instance=RequestContext(request))

def addbook(request):
	if request.user.is_authenticated():
		form = AddBookForm()
		if request.method == 'POST':
			form = AddBookForm(request.POST)
			if form.is_valid():
				book_id = form.cleaned_data.get('book_id',0)
				book_name = form.cleaned_data['book_name']
				count = form.cleaned_data['count']
				author = form.cleaned_data['author']
				try:
					book_object = Books.objects.get(book_id=book_id)
					error_msg = "That ID is Already Taken"
					return render_to_response('library/addbook.html',{'form':form, 'error_msg':error_msg}, context_instance=RequestContext(request))
				except ObjectDoesNotExist:
					try:
						book_object = Books.objects.get(book_name=book_name)
						error_msg = "A Entry Already Exists With same Name"
						return render_to_response('library/addbook.html', {'form':form, 'error_msg':error_msg}, context_instance=RequestContext(request))
					except ObjectDoesNotExist:
						new_book = Books(book_id=book_id, book_name=book_name, count=count, author=author)
						new_book.save()
						flag = 1
						msg = "Book successsfully Added"
						return render_to_response('library/addbook.html', {'flag':flag, 'form':form, 'msg':msg}, context_instance=RequestContext(request))
			else:
				return render_to_response('library/addbook.html', {'form':form}, context_instance=RequestContext(request))
			
		else:
			form = AddBookForm()
			return render_to_response('library/addbook.html', {'form':form}, context_instance=RequestContext(request))	
	else:
		HttpResponseRedirect('/login/')

		
def addstudent(request):
	if request.user.is_authenticated():
		form = AddStudentForm()
		if request.method == 'POST':
			form = AddStudentForm(request.POST)
			if form.is_valid():
				s_id = form.cleaned_data.get('s_id', 0)
				name = form.cleaned_data['name']
				email = form.cleaned_data['email']
				try:
					student_object = Students.objects.get(s_id=s_id)
					error_msg = "That Student ID is Already Taken"
					return render_to_response('library/addstudent.html', {'form':form, 'error_msg':error_msg}, context_instance=RequestContext(request))
				except ObjectDoesNotExist:
					try:
						student_object = Students.objects.get(email=email)
						error_msg = "That email is already associated with another account"
						return render_to_response('library/addstudent.html', {'form':form, 'error_msg':error_msg}, context_instance=RequestContext(request))
					except ObjectDoesNotExist:
						new_student = Students(s_id=s_id, name=name, email=email)
						new_student.save()
						flag = 1
						msg = "New Student is successsfully added"
						return render_to_response('library/addstudent.html', {'form':form, 'msg':msg}, context_instance=RequestContext(request))
			else:
				return render_to_response('library/addstudent.html', {'form':form}, context_instance=RequestContext(request))
		else:
			return render_to_response('library/addstudent.html', {'form':form}, context_instance=RequestContext(request))
	else:
		HttpResponseRedirect('/login/')

def studentdetail(request):
	try:
		sid = request.POST.get('s_id',0 )
		s = Students.objects.get(s_id=sid)
		i = BookIssued.objects.filter(s_id__s_id = sid)
		return render_to_response('library/studentdetail.html', {'student':s, 'books':i}, context_instance=RequestContext(request))
	except ObjectDoesNotExist:
		error_msg = "Incorrect Student ID"
		return render_to_response('library/login.html', {'error_msg':error_msg} , context_instance=RequestContext(request))
	

