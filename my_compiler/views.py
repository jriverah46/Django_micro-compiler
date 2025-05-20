from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Codefile

from my_compiler.compiler_core.lexer import lexer, lexical_errors, tokenize_code
from my_compiler.compiler_core.parser import parser, SyntaxErrorException
from my_compiler.compiler_core.interpreter import Interpreter

import json
import pickle
import base64


def home(request):
    return render(request, "index.html")


def editor(request):
    return render(request, "editor.html")


def compile(request):
    if request.method == "POST":
        code = request.POST.get("code", "").replace("\r\n", "\n").strip()
        
        # Restablecer errores léxicos
        lexical_errors.clear()
        lexer.lineno = 1
        
        try:
            # Análisis léxico
            lexer.input(code)
            while True:
                tok = lexer.token()
                if not tok:
                    break
            
            if lexical_errors:
                return JsonResponse({
                    'success': False,
                    'output': "Errores léxicos encontrados:\n" + "\n".join(lexical_errors)
                })
            
            # Análisis sintáctico (genera el AST real)
            ast = parser.parse(code, lexer=lexer)
            
            # Debug: Mostrar el AST generado
            print("AST generado:", ast)
            
            return JsonResponse({
                'success': True,
                'output': "Compilación exitosa",
                'ast': ast  # Enviar el AST real, no el mensaje
            })
            
        except SyntaxErrorException as e:
            return JsonResponse({
                'success': False,
                'output': f"Error de sintaxis: {str(e)}"
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'output': f"Error inesperado: {str(e)}"
            })
    
    return JsonResponse({'success': False, 'output': 'Método no permitido'})


def initialize_interpreter():
    return Interpreter()


def execute(request):
    if request.method == "POST":
        try:
            # Obtener datos del request
            ast_json = request.POST.get("ast", "")
            code = request.POST.get("code", "")
            
            # Debug: Mostrar el AST recibido
            print("\n" + "="*50)
            print("AST recibido (raw):", ast_json)
            
            # Convertir el AST de string a objeto Python
            try:
                ast = json.loads(ast_json)
                # Si el AST viene como string, intentar parsear nuevamente
                if isinstance(ast, str):
                    ast = json.loads(ast)
            except json.JSONDecodeError as e:
                print(f"Error decodificando AST: {str(e)}")
                raise
            
            # Debug: Mostrar el AST parseado
            print("\nAST parseado:", ast)
            print("Tipo del AST:", type(ast))
            if isinstance(ast, (list, dict)):
                print("Longitud del AST:", len(ast))
            
            # Crear y configurar intérprete
            interpreter = Interpreter()
            
            # Debug: Mostrar estado antes de ejecutar
            print("\nIniciando ejecución...")
            
            # Ejecutar el código
            output = interpreter.execute(ast)
            
            # Debug: Mostrar resultados
            print("\nEjecución completada")
            print("Variables finales:", interpreter.get_variables())
            print("Salida generada:", output)
            print("Pasos de ejecución:", interpreter.execution_steps)
            
            # Preparar respuesta
            response_data = {
                'success': True,
                'output': "\n".join(output) if output else "Ejecución completada sin salida",
                'variables': interpreter.get_variables(),
                'steps': interpreter.execution_steps
            }
            
            # Debug: Mostrar datos que se enviarán
            print("\nDatos de respuesta:", response_data)
            print("="*50)
            
            return JsonResponse(response_data)
            
        except json.JSONDecodeError as e:
            error_msg = f"Error al decodificar AST: {str(e)}"
            print(error_msg)
            return JsonResponse({
                'success': False,
                'error': error_msg
            })
            
        except Exception as e:
            error_msg = f"Error en ejecución: {str(e)}"
            print(error_msg)
            import traceback
            traceback.print_exc()  # Imprimir traceback completo
            return JsonResponse({
                'success': False,
                'error': error_msg
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Método no permitido'
    })
            
def save_file(request):
    if request.method == "POST":
        name = request.POST.get("name")
        code = request.POST.get("code")
        from_editor = request.POST.get("from_editor")

        if from_editor:
            return render(request, "save_file.html", {"code": code})

        try:
            existing = Codefile.objects.get(name=name)
            if not request.POST.get("confirm"):
                return render(request, "confirm_overwrite.html", {
                    "name": name, "code": code
                })
            existing.code = code
            existing.save()
        except Codefile.DoesNotExist:
            Codefile.objects.create(name=name, code=code)

        return redirect("files")

    return render(request, "save_file.html")


def tokens(request):
    if request.method == "POST":
        code = request.POST.get("code", "")
        tokens = tokenize_code(code)
        return render(request, "tokens.html", {"tokens": tokens, "code": code})

    action = request.GET.get("action")
    if action == "back":
        code = request.GET.get("code", "")
        return render(request, "editor.html", {"code": code})
    return render(request, "tokens.html", {"tokens": []})


def files_list(request):
    files = Codefile.objects.all()
    return render(request, "files.html", {"files": files})


def delete_file(request, file_id):
    file = get_object_or_404(Codefile, id=file_id)
    file.delete()
    return redirect("files")


def open_file(request, file_id):
    file = get_object_or_404(Codefile, id=file_id)
    code = file.code
    name = file.name
    action = request.GET.get('action')

    if action == 'compile':
        return render(request, 'editor.html', {'code': code})

    return render(request, "confirm_overwrite.html", {
        "name": name, "code": code
    })


def new_file(request):
    return render(request, "editor.html")

