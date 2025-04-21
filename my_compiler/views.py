from django.shortcuts import render,redirect,get_object_or_404
from my_compiler.compiler_core.parser import parser,SyntaxErrorException
from my_compiler.compiler_core.lexer import lexer,lexical_errors,tokenize_code
from .models import Codefile

# Create your views here.

def home(request):
    return render(request,"index.html")

def editor(request):
    return render(request,"editor.html")

def compile(request):
    if request.method=="POST":
        code=request.POST.get("code","")
        
        
        # Limpiar saltos de línea extra
        
        code = code.replace("\r\n", "\n").replace('\r', '\n').strip()  
        print(repr(code))
        # Eliminar cualquier espacio en blanco adicional al principio o al final
        
          # Reiniciar errores antes de compilar
        lexical_errors.clear()

        try:
            lexer.lineno = 1
            # Ejecutar el lexer para poblar lexical_errors
            lexer.input(code)
            
            while lexer.token():
                pass

            # Si hay errores léxicos, no compilamos
            if lexical_errors:
                output = "Errores léxicos encontrados:\n" + "\n".join(lexical_errors)
            else:
                # Si no hay errores léxicos, proceder al parser
                result = parser.parse(code, lexer=lexer)
                output = f"Código compilado exitosamente. Resultado: {result}"
                
        except SyntaxErrorException as e:
            output = f"Error durante compilación: {str(e)}"        
        except Exception as e:
            output = f"Error durante compilación: {str(e)}"
            
        return render(request,"compile_result.html",{"result":output,"code":code})
    
    action = request.GET.get('action')
    if action=="volver":
        code = request.GET.get("code", "")
        return render(request, "editor.html", {"code": code})
        
            
def save_file(request):
    if request.method == "POST":
        name = request.POST.get("name")
        code = request.POST.get("code")
        from_editor = request.POST.get("from_editor")  # Verificar si viene desde el editor

        # Si viene desde el editor, precargar el código en el formulario
        if from_editor:
            return render(request, "save_file.html", {"code": code})

        # Validar si ya existe el archivo
        try:
            existing = Codefile.objects.get(name=name)
            # Si existe y no se envió confirmación, preguntar
            if not request.POST.get("confirm"):
                return render(request, "confirm_overwrite.html", {
                    "name": name,
                    "code": code
                })
            # Si el usuario confirmó, sobrescribir
            existing.code = code
            existing.save()
        except Codefile.DoesNotExist:
            # Si no existe, crear
            Codefile.objects.create(name=name, code=code)

        return redirect("files")

    return render(request, "save_file.html")
        

def tokens(request):
    if request.method == "POST":
        code = request.POST.get("code", "")
        tokens = tokenize_code(code)
        return render(request, "tokens.html", {"tokens": tokens, "code": code})
    
    action=request.GET.get("action")
    if action=="back":
        code = request.GET.get("code", "")
        return render(request, "editor.html", {"code": code})
    return render(request, "tokens.html", {"tokens": []})

def files_list(request):
    files=Codefile.objects.all()
    return render(request,"files.html",{"files":files})
    

def delete_file(request,file_id):
    file=get_object_or_404(Codefile,id=file_id)
    file.delete()
    return redirect("files")

def open_file(request,file_id):
    file=get_object_or_404(Codefile,id=file_id)
    code=file.code
    name=file.name
    action = request.GET.get('action')
    
    if action == 'compile':
        return render(request, 'editor.html', {'code': code})
    
    return render(request, "confirm_overwrite.html", {
                    "name": name,
                    "code": code
                })
    
def new_file(request):
    return render(request,"editor.html")
