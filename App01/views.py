import subprocess
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render,HttpResponse
import os
import tempfile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
import json
from .models import questions,in_out,sub
from django.shortcuts import render,redirect,HttpResponse
from .models import *
from .forms import *
import pandas as pd
from django.core.files.storage import FileSystemStorage
# Create your views here.
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout 
from Project01.settings import BASE_DIR
from functools import wraps

def session_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Check if any of 'email', 'enroll', or 'admin_id' is in the session
        if not any(key in request.session for key in ['email', 'enroll', 'admin_id']):
            # Redirect to the login page if none of these keys are present
             return render(request, 'loginPage.html', {'error1': 'Need To login Frist'})# Ensure 'login' matches your URL pattern name

        # If one of them is present, proceed with the view
        return view_func(request, *args, **kwargs)

    return wrapper

#_Total=0
def logout_view(request):
    request.session.flush()
    return redirect('login')

def index(request):
    return render(request, 'index_new.html')
@session_required 
def addcourse(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name', '').strip()
        
        if course_name:
            new_course = courses.objects.create(course_name=course_name)
            print(f"Course added: {course_name}")
            return HttpResponse(f"Course '{course_name}' added successfully!")
        else:
            return HttpResponse("Please enter a course name.")
            
    return render(request, 'addcourses.html')

@session_required            
def practice(request):
    return render(request, 'practice.html')


def LandingPage(request):
    return render(request, 'Landing.html')
@session_required 
def UserIndex(request):
    enroll_no = request.session.get('enroll')
    try:
        stu = stu_details.objects.get(enroll=enroll_no)
    except stu_details.DoesNotExist:   
        return render(request, 'loginPage.html')
    
    return render(request, 'userIndex.html',{'student':stu})

def Click(request):
    return render(request, 'Click.html')

def Login(request):
    return render(request, 'loginPage.html')

@session_required
def StudentSignup(request):
    course = courses.objects.all()
    return render(request, 'StudentSignupex.html', {'course': course})
# from django.contrib.auth.decorators import login_required

# @login_required
@session_required
def Stu_list(request):
    Show = stu_details.objects.all()
    return render(request, 'tables.html', {'Show': Show})
@session_required
def teach_list(request):
    teach = Registration_t.objects.all()
    return render(request, 'teach_list.html', {'teach': teach})
def delete_student(request):
    if request.method == "POST":
        stu_id=request.POST['id']
        dele = get_object_or_404(stu_details, stu_id=stu_id)
        if request.method == "POST":
            dele.delete()
            return redirect('Showstu')
        return redirect('Showstu')

def delete_teach(request):
    if request.method == "POST":
        t_id=request.POST['id']
        dele = get_object_or_404(Registration_t, t_id=t_id)
        if request.method == "POST":
            dele.delete()
            return redirect('teach_list')
        return redirect('teach_list')
@session_required   
def superadmin(request):
    student_count = stu_details.objects.count()
    teach_count = Registration_t.objects.count()
    admin_id = request.session.get('admin_id')
    
    try: 
        admin =  Admin_log.objects.get(admin_id=admin_id) 
    except Admin_log.DoesNotExist:
        return render(request, 'loginPage.html')
    context = {
        'student_count': student_count,
        'teach_count': teach_count,
        'admin_id': admin_id
    }
    
    return render(request, 'Admin.html', context)
@session_required
def register(request):
    if request.method == "POST":
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        email = request.POST['email']
        phone = request.POST['phone']
        sub_id = request.POST['sub_id']
        experience = request.POST['experience']
        address = request.POST['address']
        teach_pass = request.POST['teach_pass']

        subject = sub.objects.get(pk=sub_id)
        
        new_user = Registration_t.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            sub_id=subject,
            experience=experience,
            address=address,
            teach_pass=make_password(teach_pass)  # Hash the password
        )
        return HttpResponse("Registration successful!")
    
    Subject = sub.objects.all()
    return render(request, 'teach.html', {'Subject': Subject})
    
def edit_student_data(request):
    if request.method == "POST":
        stu_id=request.POST['id']
    i = get_object_or_404(stu_details, stu_id=stu_id)
    if request.method == 'POST':
        form = SignupForm(request.POST, instance=i)
        if form.is_valid():
            form.save()
            return redirect('Showstu')
    else:
        form = SignupForm(instance=i)
    return render(request, 'editstu.html', {'form': form, 'i': i})

def edit_stu_save(request):
    if request.method =='POST':
        stuid=request.POST['id']
        stu =  stu_details.objects.get(stu_id=stuid)
        stu.name= request.POST.get('name', '').strip()
        stu.email = request.POST.get('Email', '').strip()
        stu.age=request.POST.get('age', '').strip()
        stu.div=request.POST.get('Division', '').strip()
        stu.enroll=request.POST.get('Enroll', '').strip()
        stu.roll_no=request.POST.get('Roll', '').strip()
        course_instance = courses.objects.get(pk=request.POST.get('Course', '').strip())
        stu.course_id=course_instance
        stu.stu_pass=request.POST.get('password', '').strip()
        stu.course_id = courses.objects.get(pk=1)
        stu.save()
        return HttpResponse("updated")

def edit_teach_data(request):
    t_id = request.POST.get('id', None)
    i = get_object_or_404(Registration_t, t_id=t_id)
    
    if request.method == 'POST':
        form = teachform(request.POST, instance=i)
        if form.is_valid():
            form.save()
            return redirect('teach_list')
    else:
        form = teachform(instance=i)
    
    return render(request, 'editteach.html', {'form': form, 'i': i})

def edit_teach_save(request):
    if request.method == 'POST':
        tid = request.POST.get('id', None)
        try:
            stu = Registration_t.objects.get(t_id=tid)
            stu.first_name = request.POST.get('first_name', '').strip()
            stu.last_name = request.POST.get('last_name', '').strip()
            stu.email = request.POST.get('email', '').strip()
            stu.phone = request.POST.get('phone', '').strip()
            stu.experience = request.POST.get('experience', '').strip()
            stu.address = request.POST.get('address', '').strip()
            stu.teach_pass = request.POST.get('teach_pass', '').strip()
            
            course_id = request.POST.get('Sub', None)
            if course_id:
                course_instance = sub.objects.get(pk=course_id.strip())
                stu.sub_id = course_instance
            
            stu.save()
            return HttpResponse("updated")
        except Registration_t.DoesNotExist:
            return HttpResponse("Teacher not found", status=404)
def loginPost(request):
    if request.method == 'POST':
        enroll = request.POST.get('enroll')
        password = request.POST.get('stu_pass')
        try:
            student = stu_details.objects.get(enroll=enroll)
            if check_password(password, student.stu_pass):
                request.session['enroll'] = enroll
                return redirect('UserIndex')
        except stu_details.DoesNotExist:    
            pass 

        try:
            teacher = Registration_t.objects.get(email=enroll)
            if check_password(password, teacher.teach_pass):
                request.session['email'] = enroll
                return redirect('prof')
        except Registration_t.DoesNotExist:
            pass  

        try:
            admin = Admin_log.objects.get(admin_id=enroll)
            if admin.check_password(password):  
                request.session['admin_id'] = enroll
                return redirect('superadmin')
        except Admin_log.DoesNotExist:
            pass  
        return render(request, 'loginPage.html', {'error': 'Invalid credentials'})

    return render(request, 'loginPage.html')

      

def signupPost(request):
    if request.method == "POST":
        ##fetch the inputs
        Name= request.POST.get('name', '').strip()
        Email = request.POST.get('Email', '').strip()
        Age=request.POST.get('age', '').strip()
        Div=request.POST.get('Division', '').strip()
        Enroll=request.POST.get('Enroll', '').strip()
        Roll=request.POST.get('Roll', '').strip()
        Course=request.POST.get('Course', '').strip()
        Pass=request.POST.get('password', '').strip()
        course_instance = courses.objects.get(pk=1)
        user_exists = stu_details.objects.filter(enroll=Enroll).exists()
        if user_exists :
            return redirect("signuppage")
        else :
            new_user=stu_details.objects.create(
                name=Name,
                age=Age,
                div=Div,
                enroll=Enroll,
                roll_no =Roll,
                email=Email,
                course_id=course_instance,
                stu_pass=make_password(Pass)
            )
        request.session['enroll'] = Enroll
        return HttpResponse("Welcome")

def exec_code_c(c_compile_code):
    try:
        # Create a temporary directory to store the executable
        with tempfile.TemporaryDirectory() as tmpdirname:
            executable_path = os.path.join(tmpdirname, "temp_executable")

            # Compile the C program
            compile_command = [os.path.join(BASE_DIR,"MinGW\\bin\\gcc"), "-x", "c", "-", "-o", executable_path]
            compile_process = subprocess.Popen(
                compile_command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = compile_process.communicate(c_compile_code)
            
            if compile_process.returncode != 0:
                print("Compilation failed with errors:")
                return HttpResponse(stderr)

            # Run the compiled program
            run_command = [executable_path]
            run_process = subprocess.Popen(
                run_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = run_process.communicate()

            if run_process.returncode != 0:
                print("Program execution failed with errors:")
                return HttpResponse(stderr)
            else:
                print("Program output:")
                print(stdout)
                return HttpResponse(stdout)
                pass

    except Exception as e:
        print(f"An error occurred: {e}")
    # return HttpResponse(stdout)

def exec_code_cpp(cpp_compile_code):

    
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        cpp_file = f'{tmpdir}/temp.cpp'
        executable_file = f'{tmpdir}/temp'
        
        # Write the C++ code to a temporary file
        with open(cpp_file, 'w') as f:
            f.write(cpp_compile_code)
        
        # Compile the C++ code in memory
        compile_command = [os.path.join(BASE_DIR,"MinGW\\bin\\g++"), cpp_file, '-o', executable_file]
        compile_process = subprocess.Popen(compile_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        compile_output, compile_error = compile_process.communicate()
        
        if compile_process.returncode != 0:
            # Compilation failed, print error message
            print(f'Compilation failed with error:\n{compile_error}')
            return HttpResponse(compile_error)
        else:
            # Compilation successful, now run the executable in memory
            run_command = [executable_file]
            run_process = subprocess.Popen(run_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            run_output, run_error = run_process.communicate()
            
            if run_process.returncode != 0:
                # Execution failed, print error message
                print(f'Execution failed with error:\n{run_error}')
                return HttpResponse(run_error)
            else:
                # Print the output of the C++ program
                print(f'Output:\n{run_output}')
                return HttpResponse(run_output)


import os
import subprocess
import tempfile
import json
from django.http import HttpResponse
from .models import in_out

def Check_in_out_cpp(request):
    try:
        # Fetch the row from the database
        total = 0
        out = ""
        data = json.loads(request.body.decode('utf-8'))
        cpp_compile_code = data.get('code', '')
        print(data.get('id'))
        rows = in_out.objects.filter(que_id_id=data.get('id')).values().all()

        print(cpp_compile_code)
        for row in rows:
            print(row['in_put'])

        # Create a temporary directory to store the executable
        with tempfile.TemporaryDirectory() as tmpdir:
            cpp_file = os.path.join(tmpdir, 'temp.cpp')
            executable_file = os.path.join(tmpdir, 'temp')

            # Write the C++ code to a temporary file
            with open(cpp_file, 'w') as f:
                f.write(cpp_compile_code)

            # Compile the C++ code
            compile_command = [os.path.join(BASE_DIR, "MinGW\\bin\\g++"), cpp_file, '-o', executable_file]
            compile_process = subprocess.Popen(compile_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            compile_output, compile_error = compile_process.communicate()

            if compile_process.returncode != 0:
                # Compilation failed, print error message
                print(f'Compilation failed with error:\n{compile_error}')
                return HttpResponse("Error" + compile_error)

            # Prepare the input expression
            for row in rows:
                expression = ' '.join(row['in_put'].strip("[]").replace(",", " ").split())
                print(expression)

                # Run the compiled program
                run_command = [executable_file]
                run_process = subprocess.Popen(run_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                run_output, run_error = run_process.communicate(input=expression)

                if run_process.returncode != 0:
                    # Execution failed, print error message
                    print(f'Execution failed with error:\n{run_error}')
                    return HttpResponse("Error" + run_error)
                else:
                    # Print the output of the C++ program
                    print(f'Output:\n{run_output}')
                    out += "Input :" + expression + "\nOutput : " + run_output + "\n" + "Expected : " + str(row['out_put']) + "\n"
                    if run_output.replace(" ", "") == str(row['out_put'].replace(" ", "")):
                        out += "Marks = 10\n\n"
                        total += 10
                    else:
                        out += "Marks = 0\n\n"
            
            out += "\n\n\n\t\t\tObtained Marks : " + str(total) + "\n\n"
            if total > 10:
                out += "\n\n\t\t\tStatus : Pass"
            else:
                out += "\n\t\t\tStatus : Fail"
            return HttpResponse(out)

    except Exception as e:
        print(f"An error occurred: {e}")
        return HttpResponse(f"An error occurred: {e}")

def exec_code_py(request):
    try:
        total = 0
        out = ""
        data = json.loads(request.body.decode('utf-8'))
        python_script_code = data.get('code', '')
        print(data.get('id'))
        rows = in_out.objects.filter(que_id_id=data.get('id')).values().all()
        print(python_script_code)

        with tempfile.TemporaryDirectory() as tmpdirname:
            script_path = os.path.join(tmpdirname, "temp_script.py")

            # Write the Python script to a file
            with open(script_path, 'w') as script_file:
                script_file.write(python_script_code)

            for row in rows:
                expression = ' '.join(row['in_put'].strip("[]").replace(",", " ").split())
                print(expression)

                # Run the Python script
                run_command = ["python", script_path]
                run_process = subprocess.Popen(
                    run_command,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                stdout, stderr = run_process.communicate(input=expression)

                if run_process.returncode != 0:
                    print("Program execution failed with errors:")
                    return HttpResponse("Error" + stderr)
                else:
                    print("Program output:")
                    out += "Input: " + expression + "\nOutput: " + stdout + "\nExpected: " + str(row['out_put']) + "\n"
                    if stdout.replace(" ", "") == str(row['out_put'].replace(" ", "")):
                        out += "Marks = 10\n\n"
                        total += 10
                    else:
                        out += "Marks = 0\n\n"

            out += "\n\n\n\t\t\tObtained Marks: " + str(total) + "\n\n"
            if total > 10:
                out += "\n\n\t\t\tStatus: Pass"
            else:
                out += "\n\t\t\tStatus: Fail"

            return HttpResponse(out)

    except Exception as e:
        print(f"An error occurred: {e}")
        return HttpResponse(f"An error occurred: {e}")


# def exec_code_java(java_program_code):
#     try:
#         # Create a temporary directory to store the Java files
#         class_name="main"
#         with tempfile.TemporaryDirectory() as tmpdirname:
#             source_file_path = os.path.join(tmpdirname, f"{class_name}.java")

#             # Write the Java program to a file
#             with open(source_file_path, 'w') as source_file:
#                 source_file.write(java_program_code)

#             # Compile the Java program
#             compile_command = ["javac", source_file_path]
#             compile_process = subprocess.Popen(
#                 compile_command,
#                 stdout=subprocess.PIPE,
#                 stderr=subprocess.PIPE,
#                 text=True
#             )
#             stdout, stderr = compile_process.communicate()

#             if compile_process.returncode != 0:
#                 print("Compilation failed with errors:")
#                 print(stderr)
#                 return

#             # Run the compiled Java program
#             run_command = ["java", "-cp", tmpdirname, class_name]
#             run_process = subprocess.Popen(
#                 run_command,
#                 stdout=subprocess.PIPE,
#                 stderr=subprocess.PIPE,
#                 text=True
#             )
#             stdout, stderr = run_process.communicate()

#             if run_process.returncode != 0:
#                 print("Program execution failed with errors:")
#                 return HttpResponse(stderr)
#             else:
#                 return HttpResponse(stdout)
#                 pass

#     except Exception as e:
#         print(f"An error occurred: {e}")



def Check_in_out_Java(request):
    try:
        print("")
        # Fetch the row from the database
        total = 0
        out = ""
        data = json.loads(request.body.decode('utf-8'))
        java_program_code = data.get('code', '')
        print("Java",data.get('id'))
        rows = in_out.objects.filter(que_id_id=data.get('id')).values().all()

        print(java_program_code)
        for row in rows:
            print(row['in_put'])

        # Create a temporary directory to store the Java files
        with tempfile.TemporaryDirectory() as tmpdirname:
            class_name = "Main"  # Ensure this matches your Java class name
            source_file_path = os.path.join(tmpdirname, f"{class_name}.java")

            # Write the Java program to a file
            with open(source_file_path, 'w') as source_file:
                source_file.write(java_program_code)
            
            # Compile the Java program
            compile_command = [".\\Java\\jdk-21\\bin\\javac.exe", source_file_path]
            compile_process = subprocess.Popen(
                compile_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = compile_process.communicate()

            if compile_process.returncode != 0:
                print("Compilation failed with errors:")
                return HttpResponse("Error" + stderr)

            # Prepare the input expression
            for row in rows:
                expression = ' '.join(row['in_put'].strip("[]").replace(",", " ").split())
                print(expression)

                # Run the compiled Java program
                run_command = [".\\Java\\jdk-21\\bin\\java.exe", "-cp", tmpdirname, class_name]
                run_process = subprocess.Popen(
                    run_command,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                stdout, stderr = run_process.communicate(input=expression)

                if run_process.returncode != 0:
                    print("Program execution failed with errors:")
                    return HttpResponse("Error" + stderr)
                else:
                    print("Program output:")
                    out += "Input :" + expression + "\nOutput : " + stdout + "\n" + "Expected : " + str(row['out_put']) + "\n"
                    if stdout.replace(" ", "") == str(row['out_put'].replace(" ", "")):
                        out += "Marks = 10\n\n"
                        total += 10
                    else:
                        out += "Marks = 0\n\n"
            
            out += "\n\n\n\t\t\tObtained Marks : " + str(total) + "\n\n"
            if total > 10:
                out += "\n\n\t\t\tStatus : Pass"
            else:
                out += "\n\t\t\tStatus : Fail"
            return HttpResponse(out)

    except Exception as e:
        print(f"An error occurred: {e}")
        return HttpResponse(f"An error occurred: {e}")

from django.shortcuts import render, get_object_or_404
@session_required
def my_django_view(request):
    
    if request.method == 'POST':
        # Your logic here
        
        # print(compile_code)
        data = json.loads(request.body.decode('utf-8'))
        compile_code = data.get('code', '')
        print(compile_code)
        lang=questions.objects.filter(que_id=data.get('id')).values('sub_id_id').first()
        print(lang['sub_id_id'],"Hello")
        print(type(lang['sub_id_id']))
        if lang['sub_id_id'] == 1:
            response=Check_Input_Output(request)
        elif lang['sub_id_id'] == 2:
             response=Check_in_out_cpp(request)
        elif lang['sub_id_id'] == 3:
             response=Check_in_out_Java(request)
        else:
            response=exec_code_py(request)
        return HttpResponse(response)
    return HttpResponse('Invalid request', status=400)
@session_required
def db_get_question(request,language):
    # ,que_id__in=[5,1,2]
    sub_name=sub.objects.filter(sub_names=language).values().first()
    print(sub_name,"asdasdd")
    db_que = questions.objects.filter(sub_id_id=sub_name['sub_id']).order_by('?').values().first()
    que_in_out=in_out.objects.filter(que_id_id=db_que['que_id']).order_by('?').values().first()
    subject=sub.objects.filter(sub_id=db_que['sub_id_id']).values().first()
    # print(subject['sub_names'])
    # print(que_in_out)
    # print(db_que)
    # for question in db_que:
    # print("Question Field1:", db_que['question_main'])
    return render(request, 'index_new.html',{'db_que':db_que,'in_out':que_in_out,'language': subject['sub_names']})
    # return request




def Check_Input_Output(request):
    # try:
    #     c_compile_code=request.POST.get('code')
    #     # Create a temporary directory to store the executable
    #     with tempfile.TemporaryDirectory() as tmpdirname:
    #         executable_path = os.path.join(tmpdirname, "temp_executable")

    #         # Compile the C program
    #         compile_command = [os.path.join(BASE_DIR,"MinGW\\bin\\gcc"), "-x", "c", "-", "-o", executable_path]
    #         compile_process = subprocess.Popen(
    #             compile_command,
    #             stdin=subprocess.PIPE,
    #             stdout=subprocess.PIPE,
    #             stderr=subprocess.PIPE,
    #             text=True
    #         )
    #         stdout, stderr = compile_process.communicate(c_compile_code)
            
    #         if compile_process.returncode != 0:
    #             print("Compilation failed with errors:")
    #             return HttpResponse(stderr)

    #         # Run the compiled program
    #         run_command = [executable_path]
    #         run_process = subprocess.Popen(
    #             run_command,
    #             stdout=subprocess.PIPE,
    #             stderr=subprocess.PIPE,
    #             text=True
    #         )
    #         stdout, stderr = run_process.communicate()

    #         if run_process.returncode != 0:
    #             print("Program execution failed with errors:")
    #             return HttpResponse(stderr)
    #         else:
    #             print("Program output:")
    #             print(stdout)
    #             return HttpResponse(stdout)
    #             pass

    # except Exception as e:
    #     print(f"An error occurred: {e}")
    # # return HttpResponse(stdout)

   
    try:
        # Fetch the row from the database
        total=0
        out=""
        data = json.loads(request.body.decode('utf-8'))
        c_compile_code = data.get('code', '')
        print(data.get('id'))
        rows = in_out.objects.filter(que_id_id=data.get('id')).values().all()
        # Get the code and the input
        print(c_compile_code)
        for row in rows :
            print(row['in_put'])
        # Create a temporary directory to store the executable
        with tempfile.TemporaryDirectory() as tmpdirname:
            executable_path = os.path.join(tmpdirname, "temp_executable")

            # Compile the C program
            compile_command = [os.path.join(BASE_DIR,"MinGW\\bin\\gcc"), "-x", "c", "-", "-o", executable_path]
            compile_process = subprocess.Popen(
                compile_command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            stdout, stderr = compile_process.communicate(c_compile_code)

            if compile_process.returncode != 0:
                print("Compilation failed with errors:")
                return HttpResponse("Error"+stderr)
        
            # Prepare the input expression
            for row in rows:
                expression = ' '.join(row['in_put'].strip("[]").replace(","," ").split())
                print(expression)
            # Run the compiled program
                run_command = [executable_path]
                run_process = subprocess.Popen(
                    run_command,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                stdout, stderr = run_process.communicate(input=expression)

                if run_process.returncode != 0:
                    print("Program execution failed with errors:")
                    return HttpResponse("Error"+stderr)
                else:
                    print("Program output:")
                    out+="Input :" + expression + "\nOutput : " + stdout + "\n" + "Expected : " + str(row['out_put']) + "\n"
                    if stdout.replace(" ","") == str(row['out_put'].replace(" ", "")):
                        out+="Marks = 10\n\n"
                        total+=5
                    else :
                        out+="Marks = 0\n\n"
            out+="\n\n\n\t\t\tObtained Marks : " + str(total) + "\n\n"
            global _Total
            _Total=total
            
            if(total>5):
                out+="\n\n\t\t\tStatus : Pass"
            else :
               out+="\n\t\t\tStatus : Fail"
            return HttpResponse(out)

    except Exception as e:
        print(f"An error occurred: {e}")
        return HttpResponse(f"An error occurred: {e}")
@session_required
def bulkstu(request):
    if request.method == 'POST' and request.FILES.get('excel_file', None):
        excel_file = request.FILES['excel_file']
        fs = FileSystemStorage()
        filename = fs.save(excel_file.name, excel_file)
        file_path = fs.path(filename)

        try:
            # Read Excel file into a DataFrame
            data = pd.read_excel(file_path, engine='openpyxl')

            # Process each row in the DataFrame
            for index, row in data.iterrows():
                # Get or create the course object
                course, created = courses.objects.get_or_create(course_id=row['course_id'])

                # Create student details entry
                stu_details.objects.create(
                    name=row['name'],
                    age=row['age'],
                    div=row['div'],
                    enroll=row['enroll'],
                    email=row['email'],
                    stu_pass=make_password(row['stu_pass']),  
                    roll_no=row['roll_no'],
                    course_id=course
                )
            
            fs.delete(filename)  # Delete the file after processing
            return HttpResponse("Successfully uploaded and processed students.")

        except Exception as e:
            fs.delete(filename)  # Ensure file deletion on error
            return HttpResponse(f"Error processing file: {e}")
    
    return render(request, 'bulk_stu.html') 

@session_required 
def prof_main(request):
    email = request.session.get('email')
    try:
        teacher = Registration_t.objects.get(email=email)
    except Registration_t.DoesNotExist:
        return redirect('login')

    return render(request, 'professor_main.html', {'teacher': teacher})
@session_required 
def add_test(request):
     return render(request, 'test.html')



# from django.shortcuts import render
# from django.utils import timezone
# from datetime import datetime
# import random

# from django.shortcuts import render
# from django.utils import timezone
# from datetime import datetime
# import random

# def add_test_post(request):
#     if request.method == "POST":
#         test_title = request.POST['testTitle']
#         test_description = request.POST['testDescription']
#         test_date = request.POST['testDate']
#         test_time = request.POST['testDuration']
#         division = request.POST['division']
#         language = request.POST['language']
#         difficulty = int(request.POST.get('difficulty'))  # Ensure difficulty is an integer

#         # Combine test_date and test_time into a single datetime object
#         test_datetime_str = f"{test_date} {test_time}"
#         test_datetime = datetime.strptime(test_datetime_str, '%Y-%m-%d %H:%M')

#         # Make test_datetime offset-aware
#         test_datetime = timezone.make_aware(test_datetime)

#         # Get the current datetime
#         current_datetime = timezone.now()

#         # Validate date and time
#         if test_datetime < current_datetime:
#             error_message = "The test date and time must be in the future."
#             return render(request, 'test.html', {
#                 'testTitle': test_title,
#                 'testDescription': test_description,
#                 'testDate': test_date,
#                 'testDuration': test_time,
#                 'division': division,
#                 'language': language,
#                 'difficulty': difficulty,
#                 'error_message': error_message,
#             })

#         # Create a new exam
#         try:
#             new_exam = exam.objects.create(
#                 sub_id=sub.objects.filter(sub_names=language).first(),
#                 exam_time=test_time,
#                 exam_date=test_date,
#                 description=test_description,
#                 duration=datetime.strptime(test_time, '%H:%M').time(),
#             )
#         except Exception as e:
#             return render(request, 'test.html', {'error_message': f"Error creating exam: {str(e)}"})

#         students = stu_details.objects.filter(div=division)

#         for student in students:
#             questions_part1 = []
#             questions_part2 = []
#             Questions = []

#             # Fetch questions based on difficulty
#             if difficulty == 4:
#                 questions_part1 = list(questions.objects.filter(difficulty_level__in=[3, 4], 
#                             sub_id_id=sub.objects.filter(sub_names=language).first().sub_id).order_by('?')[:4])
#                 questions_part2 = list(questions.objects.filter(difficulty_level=2, 
#                             sub_id_id=sub.objects.filter(sub_names=language).first().sub_id).order_by('?')[:1])
#             elif difficulty == 3:
#                 questions_part1 = list(questions.objects.filter(difficulty_level__in=[2, 3], 
#                             sub_id_id=sub.objects.filter(sub_names=language).first().sub_id).order_by('?')[:3])
#                 questions_part2 = list(questions.objects.filter(difficulty_level=2, 
#                             sub_id_id=sub.objects.filter(sub_names=language).first().sub_id).order_by('?')[:2])
#             elif difficulty == 2:
#                 questions_part1 = list(questions.objects.filter(difficulty_level=2, 
#                             sub_id_id=sub.objects.filter(sub_names=language).first().sub_id).order_by('?')[:5])

#             Questions = questions_part1 + questions_part2

#             # Ensure we have exactly 5 questions
#             if len(Questions) == 5:
#                 random.shuffle(Questions)

#                 # Create exam for student
#                 try:
#                     exam_stu.objects.create(
#                         test=new_exam,
#                         stu_id=stu_details.objects.get(stu_id=student.stu_id),
#                         q1=Questions[0].que_id,
#                         q2=Questions[1].que_id,
#                         q3=Questions[2].que_id,
#                         q4=Questions[3].que_id,
#                         q5=Questions[4].que_id,
#                     )
#                 except Exception as e:
#                     return render(request, 'test.html', {'error_message': f"Error creating exam for student {student.stu_id}: {str(e)}"})

#                 # Initialize marks in Mark table
#                 try:
                    
#                     mark=Mark.objects.create(
#                         total_marks=0,
#                         student_id=student.stu_id,
#                         test_id=new_exam
#                     )
#                     mark.save()
#                     # Initialize marks in MarkDetail table for each question
#                     for question in Questions:
#                         mark_detail=MarkDetail.objects.create(
#                             marks_obtained=0,
#                             question_id=question.que_id,
#                             student_id=student.stu_id,
#                             test_id=new_exam
#                         )
#                         mark_detail.save()
#                 except Exception as e:
#                     return render(request, 'test.html', {'error_message': f"Error initializing marks: {str(e)}"})

#         return render(request, 'test.html', {'flag': 1})

#     return render(request, 'test.html')


# -- Create the table
# CREATE TABLE StarPatterns (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     pattern TEXT
# );

# -- Insert a pattern
# INSERT INTO StarPatterns (pattern) VALUES ('*\n**\n***\n****\n*****');


from django.db.models import Subquery
from django.db.models import Q

from datetime import datetime, timedelta, timezone
from django.shortcuts import render
@session_required 
def ListQuestions(request, examid):
    # stu= stu_details.objects.filter(enroll=request.session.get('enroll',None)).values('stu_id').first()
    # print(stu, "asdjkbaksbd")
    stu=8
    student = stu_details.objects.filter(stu_id=stu).first()
    MarksDetails = MarkDetail.objects.filter(student_id=stu, test_id=examid).values_list('question_id', flat=True)
    MarksDetails = list(MarksDetails)
    print(MarksDetails)
    exam_detail = exam.objects.filter(exam_id=examid).select_related('sub_id').first()
    print(exam_detail.exam_id)
    if True:
        # Combine exam_date and exam_time to get the full start datetime
        exam_start_datetime = datetime.combine(exam_detail.exam_date, exam_detail.exam_time)
        
        # Calculate end time
        duration = timedelta(
            hours=exam_detail.duration.hour,
            minutes=exam_detail.duration.minute,
            seconds=exam_detail.duration.second
        )
        exam_end_datetime = exam_start_datetime + duration
        
        # Convert datetime to ISO string for JavaScript
        exam_start_datetime_iso = exam_start_datetime.isoformat()
        exam_end_datetime_iso = exam_end_datetime.isoformat()
        
        # Add these to the context
        exam_detail.exam_start_datetime_iso = exam_start_datetime_iso
        exam_detail.exam_end_datetime_iso = exam_end_datetime_iso
        
        _id = stu_details.objects.filter(enroll=123).values_list('stu_id', flat=True)
        distinct_q_ids = exam_stu.objects.filter(stu_id_id__in=_id,test_id=examid).values_list('q1', 'q2', 'q3', 'q4', 'q5').distinct()
        distinct_q_ids = list(set([q for sublist in distinct_q_ids for q in sublist if q is not None]))
        filtered_questions = questions.objects.filter(que_id__in=distinct_q_ids)    
        
        return render(request, "list.html", {
            'questions': filtered_questions,
            'exam': exam_detail,
            'MarksDetails':MarksDetails
        })
    else:
        # Handle the case where exam_detail is None
        return render(request, "list.html", {
            'questions': [],
            'exam': None,
            'MarksDetails': None
        })
def solve_question(request, que_id,exam_id):
    sub_id=questions.objects.filter(que_id=que_id).values().first()
    sub_name=sub.objects.filter(sub_id=sub_id['sub_id_id']).values().first()
    print(sub_name,"asdasdd")
    db_que = questions.objects.filter(que_id=que_id).values().first()
    que_in_out=in_out.objects.filter(que_id_id=db_que['que_id']).order_by('?').values().first()
    subject=sub.objects.filter(sub_id=db_que['sub_id_id']).values().first()
    # print(subject['sub_names'])
    # print(que_in_out)
    # print(db_que)
    # for question in db_que:
    # print("Question Field1:", db_que['question_main'])
    return render(request, 'index_new.html',{'db_que':db_que,'in_out':que_in_out,'language': subject['sub_names'],'exam_id':exam_id})

from django.urls import reverse
def SubmitPost(request, que_id, exam_id):
    

    stu = stu_details.objects.filter(enroll=123).first()
    if stu:
        # Create a MarkDetail instance
        MarkDetail.objects.create(    
            marks_obtained=_Total,
            question_id=que_id,
            student=stu,  # Ensure this is the correct reference
            test_id=exam_id,
        )
    
    # Fetch or create the Mark instance
    exam_instance = exam.objects.filter(exam_id=exam_id).first()
    if exam_instance:
        obj, created = Mark.objects.get_or_create(
            test=exam_instance,
            student=stu,
            defaults={'total_marks': _Total}
        )
        if not created:
            # If the record already exists, update total_marks
            obj.total_marks += _Total
            obj.save()
    
    return redirect(reverse('exam_detail', args=[exam_id]))  

        




from datetime import datetime
import random
from django.core.mail import send_mail
def add_test_post(request):
    if request.method == "POST":
        test_title = request.POST['testTitle']
        test_description = request.POST['testDescription']
        test_date = request.POST['testDate']
        test_time = request.POST['testDuration']
        division = request.POST['division']
        language = request.POST['language']
        difficulty = int(request.POST.get('difficulty'))  # Ensure difficulty is an integer
        print("Difficulty:", difficulty)
        
        # Create a new exam
        new_exam = exam.objects.create(
            sub_id=sub.objects.filter(sub_names=language).first(),
            exam_title=test_title,
            div=division,
            exam_time=test_time,
            exam_date=test_date,
            description=test_description,
            duration=str(timedelta(hours=2)),
        )
        
        students = stu_details.objects.filter(div=division).all()
        
        for student in students:
            questions_part1 = []
            questions_part2 = []
            Questions = []
            
            if difficulty == 4:
                questions_part1 = list(questions.objects.filter(difficulty_level__in=[3, 4], sub_id_id=sub.objects.filter(sub_names=language).first().sub_id).order_by('?')[:4])
                questions_part2 = list(questions.objects.filter(difficulty_level=2, sub_id_id=sub.objects.filter(sub_names=language).first().sub_id).order_by('?')[:1])
            elif difficulty == 3:
                questions_part1 = list(questions.objects.filter(difficulty_level__in=[2, 3], sub_id_id=sub.objects.filter(sub_names=language).first().sub_id).order_by('?')[:3])
                questions_part2 = list(questions.objects.filter(difficulty_level=2, sub_id_id=sub.objects.filter(sub_names=language).first().sub_id).order_by('?')[:2])
            elif difficulty == 2:
                questions_part1 = list(questions.objects.filter(difficulty_level=2, sub_id_id=sub.objects.filter(sub_names=language).first().sub_id).order_by('?')[:5])
            
            Questions = questions_part1 + questions_part2
            
            # Ensure we have exactly 5 questions
            if len(Questions) == 5:
                random.shuffle(Questions)
                
                exam_stu.objects.create(
                    test=new_exam,
                    stu_id=stu_details.objects.get(stu_id=student.stu_id),
                    q1=Questions[0].que_id,
                    q2=Questions[1].que_id,
                    q3=Questions[2].que_id,
                    q4=Questions[3].que_id,
                    q5=Questions[4].que_id,
                )
                
                # Create notification for each student
                message = f"A new test '{test_title}' has been scheduled."
                Notification.objects.create(
                    user=stu_details.objects.get(stu_id=student.stu_id),
                    message=message
                )

                mark=Mark.objects.create(
                        total_marks=0,
                        student_id=student.stu_id,
                        test_id=new_exam.exam_id
                    )
                    
                    # Initialize marks in MarkDetail table for each question
                for question in Questions:
                        mark_detail=MarkDetail.objects.create(
                            marks_obtained=0,
                            question_id=question.que_id,
                            student_id=student.stu_id,
                            test_id=new_exam.exam_id
                        )

                print(message)
                # Optionally send email notifications
                # send_mail(
                #     'New Test Notification',
                #     message,
                #     'vigljku@gmail.com',
                #     [student.email],
                #     fail_silently=False,
                # )
        
        return HttpResponse("Test added successfully!")

    return render(request, 'add_test.html')



    
# from django.contrib.auth.decorators import login_required

# @login_required
def get_notifications(request,student):
    if student:
        notifications = Notification.objects.filter(user_id=student).values()
    else:
        notifications = []
    return JsonResponse(list(notifications), safe=False)
# @require_POST
def delete_notification(request,student):
    if student:
         # Delete notifications for the given student
        Notification.objects.filter(user_id=student).delete()
    else:
        notifications = []
    return JsonResponse(list(notifications), safe=False)


def mark_notification_as_read(request):
    import json
    data = json.loads(request.body)
    notification_id = data.get('id')

    try:
        notification = Notification.objects.get(id=notification_id)
        notification.is_read = True
        notification.save()
        return JsonResponse({'status': 'success'})
    except Notification.DoesNotExist:
        return JsonResponse({'status': 'error'}, status=404)


from datetime import datetime

from datetime import datetime, timedelta
from django.shortcuts import render
@session_required 
def test_list(request):
    stu = 8
    print(stu,"asdjkbaksbd")
    student = stu_details.objects.filter(stu_id=stu).first()
    exams = exam.objects.filter(div=student.div).select_related('sub_id')

    for exam_detail in exams:
        # Combine exam_date and exam_time to get the full start datetime
        exam_start_datetime = datetime.combine(exam_detail.exam_date, exam_detail.exam_time)
        
        # Calculate end time
        duration = timedelta(hours=exam_detail.duration.hour, minutes=exam_detail.duration.minute, seconds=exam_detail.duration.second)
        exam_end_datetime = exam_start_datetime + duration
        
        # Convert datetime to ISO string for JavaScript
        exam_detail.exam_start_datetime_iso = exam_start_datetime.isoformat()
        exam_detail.exam_end_datetime_iso = exam_end_datetime.isoformat()

    return render(request, 'test_list.html', {'exams': exams})


def add_que(request):
    return render(request, 'add_que_prof.html')
def show_marks(request):
    return render(request, 'test_marks.html')
def show_marks_post(request):
    division_id = request.POST.get('division')
    subject = request.POST.get('subject')

    # Fetching the exam dates based on the division and subject
    date_list = exam.objects.filter(div=division_id, sub_id=subject).values_list('exam_date', flat=True)

    # Format the dates as strings
    formatted_dates = [date.strftime('%Y-%m-%d') for date in date_list]

    return render(request, 'test_marks.html',{'date_list':formatted_dates,}) 
from datetime import datetime
from django.utils import timezone
def search_exam(request):   
    division_id = request.POST.get('division')
    subject = request.POST.get('subject')

    sub_name=sub.objects.filter(sub_id=subject).first()
    print(sub_name.sub_names)

    date_str=request.POST.get('exam_date')
    if date_str:
        # Convert the date string to a timezone-aware datetime
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    else:
        date = None
    # print(date)
    # Filter exams using the timezone-aware date
    exam_det = exam.objects.filter(div=division_id, sub_id=subject, exam_date__date=date).first()
    
    marks_detail=Mark.objects.filter(test_id=exam_det.exam_id).values()
    stu=[]
    for mark in marks_detail:
            student = stu_details.objects.filter(stu_id=mark['student_id']).first()
            if student:
                stu.append({
                    'name': student.name,
                    'roll_no': student.roll_no,
                    'marks_obtained': mark['total_marks'],
                    'subject': sub_name.sub_names, # Assuming you want to include marks as well
                })
    print(stu)
    # print(marks_detail)
    # print(exam_det.exam_id)

    return render(request, 'test_marks.html', {'stu': stu})


import openpyxl
from django.http import HttpResponse
  # Import your models accordingly

def download_marks_excel(request):
    # Create a new Excel workbook and select the active sheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Marks'

    # Add column headers
    sheet.append(['Name', 'Roll Number', 'Marks Obtained', 'Subject'])

    # Fetch the data from the database (filter as necessary)
    division_id = request.POST.get('division')
    subject = request.POST.get('subject')
    date_str = request.POST.get('exam_date')
    if date_str:
        # Convert the date string to a timezone-aware datetime
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    else:
        date = None

    # Query exam details
    exam_det = exam.objects.filter(div=division_id, sub_id=subject, exam_date__date=date).first()
    marks_detail = Mark.objects.filter(test_id=exam_det.exam_id).values()

    # Loop through the marks and add rows to the sheet
    for mark in marks_detail:
        student = stu_details.objects.get(stu_id=mark['stu_id'])  # Assuming you have a Student model
        row = [
            student.name,
            student.roll_no,
            mark['marks_obtained'],
            mark['subject']
        ]
        sheet.append(row)

    # Prepare the HTTP response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=marks.xlsx'

    # Save the workbook to the response
    workbook.save(response)

    return response
