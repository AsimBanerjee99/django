from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import User
from .models import rowName, columnName, timeTable

# Create your views here.

def register(request):
	if request.method == 'POST':
		# Get the post parameters
		Username = request.POST['Username']
		FirstName = request.POST['FirstName']
		LastName = request.POST['LastName']
		Password = request.POST['Password']
		ConfirmPassword = request.POST['ConfirmPassword']
		email=None
		# Check for errorneous inputs
		# username should be under 10 characters
		if len(Username) > 20:
			messages.error(request, "Username should not be greater than 20")
			return redirect('register')
		
		# passwords should match
		if Password != ConfirmPassword:
			messages.error(request, "Passwords do not match")
			return redirect('register')

		# Create the user 
		newuser = User.objects.create_user(Username, email, Password)
		newuser.first_name = FirstName
		newuser.last_name = LastName
		newuser.save()
		messages.success(request, "You are now registered in this time table website")

		return redirect('register')
	return render(request, 'register.html')
	

def login_func(request):
	if request.method == 'POST':
		# Get the post parameters
		Username = request.POST['Username']
		Password = request.POST['Password']
		user = authenticate(username=Username, password=Password)

		if user is not None:
			login(request, user)
			name = user.first_name
			messages.success(request, "Logged In Successfully")
			return redirect('createtimetable')
		else:
			messages.error(request, "Invalid Credentials, Please try again")
			return redirect('login')
			
	return render(request, 'login.html')

def createtimetable(request):
	if request.user.is_authenticated:
		customer = request.user
		column = columnName.objects.filter(customer=customer)
		row = rowName.objects.filter(customer=customer).values('id')
		row_names = [content['id'] for content in row]
		if request.method == 'POST':
			if request.POST['row_col_post']=="row_post":
				new_row_id = rowName(customer=customer, name=request.POST['row_name1'])
				new_row_id.save()
				r_n = rowName.objects.filter(customer=customer, name=request.POST['row_name1']).first()
				for y in range(1,len(column)+1):
					c_n = columnName.objects.filter(customer=customer, name=request.POST['col'+str(y)]).first()	
					new_time_table = timeTable(customer=customer, row_name=r_n, column_name=c_n, item=request.POST['row_wise_col_item'+str(y)+"1"])
					new_time_table.save()
				return redirect('/createtimetable')
			elif request.POST['row_col_post']=="col_post":
				new_col_id = columnName(customer=customer, name=request.POST['new_col'])
				new_col_id.save()
				c_n = columnName.objects.filter(customer=customer, name=request.POST['new_col']).first()
				for x in range(1,len(row_names)+1):
					r_n = rowName.objects.filter(customer=customer, name=request.POST['row_of_col'+str(x)]).first()
					new_time_table = timeTable(customer=customer, row_name=r_n, column_name=c_n, item=request.POST['col_wise_row'+str(x)])
					new_time_table.save()
				return redirect('/createtimetable')
			else:
				new_table_col = columnName(customer=customer, name=request.POST['new_table_col'])
				new_table_col.save()
				new_table_row = rowName(customer=customer, name=request.POST['new_table_row'])
				new_table_row.save()
				n_t_c = columnName.objects.filter(customer=customer, name=request.POST['new_table_col']).first()
				n_t_r = rowName.objects.filter(customer=customer, name=request.POST['new_table_row']).first()
				new_table = timeTable(customer=customer, row_name=n_t_r, column_name=n_t_c, item=request.POST['new_table_item'])
				new_table.save()
				return redirect('/createtimetable')
		all_row_with_item = []
		no_of_table = timeTable.objects.filter(customer=customer).values('id')
		
		if timeTable.objects.filter(customer=customer).first()==None:
			no_table = True
			return render(request, 'createtimetable.html', {'no_table':no_table})
		else:
			for row_name in row_names:
				time_Table = timeTable.objects.filter(customer=customer, row_name=row_name)
				row_with_item = []
				row_with_item.append(str(time_Table.first().row_name)[slice(-len(str(customer)))])
				only_row_name = []
				for i in time_Table:
					only_row_name.append(i.item)
				row_with_item.append(only_row_name)
				all_row_with_item.append(row_with_item)
			if len(no_of_table)==1:
				only_one_table = True
				no_table = False
				return render(request, 'createtimetable.html', {'column':column, 'all_row_with_item':all_row_with_item,'only_one_table':only_one_table,'no_table':no_table})
			else:
				no_table = False
				only_one_table = False
				return render(request, 'createtimetable.html', {'column':column, 'all_row_with_item':all_row_with_item,'no_table':no_table,'only_one_table':only_one_table,'no_table':no_table})
	return HttpResponse('404 - Not Found')

def logout_func(request):
	logout(request)
	messages.success(request, "Logged Out Successfully")
	return redirect('/') 

def remove_row(request):
	customer = request.user
	h = rowName.objects.filter(customer=customer).values('id')
	delete_row = rowName.objects.filter(customer=customer, id=h[len(h)-1]['id'])
	delete_row_table = timeTable.objects.filter(customer=customer, row_name=delete_row.first())
	delete_row_table.delete()
	delete_row.delete()
	return redirect('/createtimetable') 

def remove_column(request):
	customer = request.user
	h = columnName.objects.filter(customer=customer).values('id')
	delete_column = columnName.objects.filter(customer=customer, id=h[len(h)-1]['id'])
	delete_column_table = timeTable.objects.filter(customer=customer, column_name=delete_column.first())
	delete_column_table.delete()
	delete_column.delete()
	return redirect('/createtimetable') 

def remove_table(request):
	customer = request.user
	# h = columnName.objects.filter(customer=customer).values('id')
	delete_table = timeTable.objects.filter(customer=customer)
	delete_row = rowName.objects.filter(customer=customer)
	delete_column = columnName.objects.filter(customer=customer)
	
	# delete_column_table = timeTable.objects.filter(customer=customer, column_name=delete_column.first())
	# delete_column_table.delete()
	delete_table.delete()
	delete_column.delete()
	delete_row.delete()
	
	return redirect('/createtimetable') 
