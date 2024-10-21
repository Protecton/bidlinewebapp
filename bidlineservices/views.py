from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
import json
import weaviate
import psycopg2
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from langchain.text_splitter import RecursiveCharacterTextSplitter
from firebase_admin import auth
# from firebase_admin.auth import InvalidIdToken
from .supabase_client import init_supabase
from .openai_client import init_openai
from decouple import config
from django.views.decorators.csrf import csrf_exempt
from random import randint
from datetime import datetime
import asyncio

from .services.supabase_service import save_response_to_supabase, get_proposal_data_by_id, save_proposal_content, save_proposal_summary
from .ai_functions.owner_name import owner_name_v1
from .ai_functions.requirements_summary import requirements_summary_v1
from .ai_functions.goals import goals_v1
from .ai_functions.dates import dates_v1
from .ai_functions.intro import intro_v1
from .ai_functions.action_plan import action_plan_v1
from .ai_functions.timeline import timeline_v1
from .ai_functions.required_extra_info import required_extra_info_v1
from .ai_functions.past_experience import past_experience_v1
from .ai_functions.closing import closing_v1

# from .models import Project, Tasks
# from .forms import CreateNewTask, CreateNewProject

# Create your views here.
def index(request):
  return HttpResponse(f'<h1>Welcome to Bidline Services</h1>')

@csrf_exempt
def get_supabase_table(request):
  supabase = init_supabase()
  response = supabase.table("users").select("*").execute()

  # Verificar que la respuesta tenga datos y que 'data' sea una lista
  if response:
    # Devuelve los datos en la respuesta JSON
    return JsonResponse({"res": response.data}, safe=False)
  else:
    return JsonResponse({"error": "No se encontraron datos"}, status=404)

@csrf_exempt
def insert_phrase(request):
  if request.method == "POST":
    try:
      # Capturar los datos enviados en el cuerpo del POST request
      data = json.loads(request.body)

      # Verificar si el campo 'content' está en los datos recibidos
      if "content" not in data:
          return JsonResponse({"error": "Falta el campo 'content' en los datos de la solicitud"}, status=400)

      content = data["content"]

      # Inicializar Supabase e insertar la frase
      supabase = init_supabase()
      insert_response = supabase.table("prompts").insert({"content": content}).execute()

      # Verificar si la inserción fue exitosa
      if insert_response.data:
          return JsonResponse({"message": "Respuesta procesada y guardada exitosamente"}, safe=False)
      else:
          return JsonResponse({"error": "Error al guardar la respuesta en la base de datos"}, status=500)

    except json.JSONDecodeError:
      return JsonResponse({"error": "Datos JSON inválidos"}, status=400)
  else:
    return JsonResponse({"error": "Método no permitido, usa POST"}, status=405)

# Bloques asíncronos
# @csrf_exempt
# async def process_supabase_openai_prompt(request):
#   try:
#     promps_notes = []
#     supabase_notes = []

#     request_body = json.loads(request.body.decode('utf-8'))

#     request_for_proposal = request_body['request_for_proposal']
#     company_info = request_body['company_info']
#     past_projects = request_body['past_projects']

#     owner_name_v1_params = [request_for_proposal]
#     requirements_summary_v1_params = [request_for_proposal]
#     goals_v1_params = [request_for_proposal]
#     dates_v1_params = [request_for_proposal]
#     intro_v1_params = [company_info, request_for_proposal]
#     action_plan_v1_params = [company_info, request_for_proposal]

#     tasks = [
#       asyncio.create_task(intro_v1(intro_v1_params)),
#       asyncio.create_task(action_plan_v1(action_plan_v1_params)),
#       asyncio.create_task(owner_name_v1(owner_name_v1_params)),
#       asyncio.create_task(requirements_summary_v1(requirements_summary_v1_params)),
#       asyncio.create_task(goals_v1(goals_v1_params)),
#       asyncio.create_task(dates_v1(dates_v1_params))
#     ]

#     completed_count = 0
#     threshold = 2  # Queremos ejecutar `next_operation` cuando 2 tareas hayan terminado
#     collected_results = []  # Lista para almacenar los resultados de las tareas completadas

#     while completed_count < threshold:
#       # Espera a que una tarea termine
#       done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

#       # Recoger los resultados de las tareas completadas
#       for task in done:
#         collected_results.append(task.result())
      
#       # Incrementar el contador de tareas completadas
#       completed_count += len(done)

#       # Actualizar las tareas pendientes
#       tasks = list(pending)

#       print(f"Tareas completadas: {completed_count}")

#     # Cuando se hayan completado el número de tareas especificadas, ejecutamos `next_operation`
#     if collected_results:
      
#       intro_response = collected_results[0]
#       action_plan_response = collected_results[1]

#       timeline_v1_params = [company_info, action_plan_response[1], request_for_proposal]
#       required_extra_info_v1_params = [company_info, action_plan_response[1], request_for_proposal, request_for_proposal]
#       past_experience_v1_params = [company_info, action_plan_response[1], request_for_proposal, past_projects, request_for_proposal]

#       timeline_response = await timeline_v1(timeline_v1_params)
#       required_extra_info_response = await required_extra_info_v1(required_extra_info_v1_params)
#       past_experience_response = await past_experience_v1(past_experience_v1_params)

#       closing_v1_params = [request_for_proposal, company_info, action_plan_response[1], past_projects, past_experience_response[1], intro_response[1]]
      
#       closing_response = await closing_v1(closing_v1_params)

#       # Esperar las tareas restantes (si las hay)
#       for task in tasks:
#         result = await task
#         collected_results.append(result)
      
#       owner_name_response = collected_results[2]
#       requirements_summary_response = collected_results[3]
#       goals_response = collected_results[4]
#       dates_response = collected_results[5]

#       if not owner_name_response:
#         promps_notes.append("No se ha procesado owner_name_v1 y por lo tanto no se han obtenido respuestas")
    
#       if not requirements_summary_response:
#         promps_notes.append("No se ha procesado requirements_summary_v1 y por lo tanto no se han obtenido respuestas")
      
#       if not goals_response:
#         promps_notes.append("No se ha procesado goals_v1 y por lo tanto no se han obtenido respuestas")
      
#       if not dates_response:
#         promps_notes.append("No se ha procesado dates_v1 y por lo tanto no se han obtenido respuestas")
      
#       if not intro_response:
#         promps_notes.append("No se ha procesado intro_v1 y por lo tanto no se han obtenido respuestas")
        
#       if not action_plan_response:
#         promps_notes.append("No se ha procesado action_plan_v1 y por lo tanto no se han obtenido respuestas")
      
#       if not timeline_response:
#         promps_notes.append("No se ha procesado timeline_v1 y por lo tanto no se han obtenido respuestas")
      
#       if not required_extra_info_response:
#         promps_notes.append("No se ha procesado required_extra_info_v1 y por lo tanto no se han obtenido respuestas")

#       if not past_experience_response:
#         promps_notes.append("No se ha procesado past_experience_v1 y por lo tanto no se han obtenido respuestas")
      
#       if not closing_response:
#         promps_notes.append("No se ha procesado closing_v1 y por lo tanto no se han obtenido respuestas")
      
#       # Guardar la respuesta en Supabase (OPCIONAL)
#       owner_name_supabase_response = save_response_to_supabase(owner_name_response[0], owner_name_response[1])
#       requirements_summary_supabase_response = save_response_to_supabase(requirements_summary_response[0], requirements_summary_response[1])
#       goals_supabase_response = save_response_to_supabase(goals_response[0], goals_response[1])
#       dates_supabase_response = save_response_to_supabase(dates_response[0], dates_response[1])
#       intro_supabase_response = save_response_to_supabase(intro_response[0], intro_response[1])
#       action_plan_supabase_response = save_response_to_supabase(action_plan_response[0], action_plan_response[1])
#       timeline_supabase_response = save_response_to_supabase(timeline_response[0], timeline_response[1])
#       required_extra_info_supabase_response = save_response_to_supabase(required_extra_info_response[0], required_extra_info_response[1])
#       past_experience_supabase_response = save_response_to_supabase(past_experience_response[0], past_experience_response[1])
#       closing_supabase_response = save_response_to_supabase(closing_response[0], closing_response[1])

#       concatenated_supabase_response = save_response_to_supabase("Intro, Proposal, Closing", f"{intro_response[1]} {action_plan_response[1]} {closing_response[1]}")
      
#       if not owner_name_supabase_response:
#         supabase_notes.append("No se han guardado las respuestas de owner_name_v1 en la base de datos")
      
#       if not requirements_summary_supabase_response:
#         supabase_notes.append("No se han guardado las respuestas de requirements_summary_v1 en la base de datos")
      
#       if not goals_supabase_response:
#         supabase_notes.append("No se han guardado las respuestas de goals_v1 en la base de datos")
      
#       if not dates_supabase_response:
#         supabase_notes.append("No se han guardado las respuestas de dates_v1 en la base de datos")
      
#       if not intro_supabase_response:
#         supabase_notes.append("No se han guardado las respuestas de intro_v1 en la base de datos")
      
#       if not action_plan_supabase_response:
#         supabase_notes.append("No se han guardado las respuestas de action_plan_v1 en la base de datos")
      
#       if not timeline_supabase_response:
#         supabase_notes.append("No se han guardado las respuestas de timeline_v1 en la base de datos")

#       if not required_extra_info_supabase_response:
#         supabase_notes.append("No se han guardado las respuestas de required_extra_info_v1 en la base de datos")

#       if not past_experience_supabase_response:
#         supabase_notes.append("No se han guardado las respuestas de past_experience_v1 en la base de datos")

#       if not closing_supabase_response:
#         supabase_notes.append("No se han guardado las respuestas de closing_v1 en la base de datos")

#       if not concatenated_supabase_response:
#         supabase_notes.append("No se han guardado las respuestas de informe concatenado en la base de datos")
      
#       if len(promps_notes) > 0 or len(supabase_notes) > 0:
#         print(promps_notes)
#         print(supabase_notes)
#         return JsonResponse({"error": "Error al guardar la respuesta en la base de datos"}, status=500)
#       else:
#         return JsonResponse({"message": "Respuesta procesada y guardada exitosamente"}, safe=False)

#     # owner_name_response = await owner_name_v1(owner_name_v1_params)
#     # requirements_summary_response = await requirements_summary_v1(requirements_summary_v1_params)
#     # goals_response = await goals_v1(goals_v1_params)
#     # dates_response = await dates_v1(dates_v1_params)
#     # intro_response = await intro_v1(intro_v1_params)
#     # action_plan_response = await action_plan_v1(action_plan_v1_params)

#     #if not owner_name_response:
#       #return JsonResponse({"message": "Error al procesar el prompt. Verifique el número de parámetros o llamadas externas."}, safe=False)
#   except NameError:
#     # print(NameError)
#     return JsonResponse({"error": "Error al procesar la solicitud en el servidor"}, status=500)

# Bloques asíncronos
@csrf_exempt
async def process_proposal(request):
  try:
    promps_notes = []
    supabase_notes = []

    request_body = json.loads(request.body.decode('utf-8'))

    proposal_id = request_body['proposal_id']

    proposal_promps = get_proposal_data_by_id(proposal_id)

    request_for_proposal = proposal_promps[0]
    company_info = proposal_promps[1]
    past_projects = proposal_promps[2]
    company_id = proposal_promps[3]

    owner_name_v1_params = [request_for_proposal]
    requirements_summary_v1_params = [request_for_proposal]
    goals_v1_params = [request_for_proposal]
    dates_v1_params = [request_for_proposal]
    intro_v1_params = [company_info, request_for_proposal]
    action_plan_v1_params = [company_info, request_for_proposal]

    tasks = [
      asyncio.create_task(intro_v1(intro_v1_params)),
      asyncio.create_task(action_plan_v1(action_plan_v1_params)),
      asyncio.create_task(owner_name_v1(owner_name_v1_params)),
      asyncio.create_task(requirements_summary_v1(requirements_summary_v1_params)),
      asyncio.create_task(goals_v1(goals_v1_params)),
      asyncio.create_task(dates_v1(dates_v1_params))
    ]

    completed_count = 0
    threshold = 2  # Queremos ejecutar `next_operation` cuando 2 tareas hayan terminado
    collected_results = []  # Lista para almacenar los resultados de las tareas completadas

    while completed_count < threshold:
      # Espera a que una tarea termine
      done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

      # Recoger los resultados de las tareas completadas
      for task in done:
        collected_results.append(task.result())
      
      # Incrementar el contador de tareas completadas
      completed_count += len(done)

      # Actualizar las tareas pendientes
      tasks = list(pending)

      # print(f"Tareas completadas: {completed_count}")

    # Cuando se hayan completado el número de tareas especificadas, ejecutamos `next_operation`
    if collected_results:
      
      intro_response = collected_results[0]
      action_plan_response = collected_results[1]

      timeline_v1_params = [company_info, action_plan_response[1][0], request_for_proposal]
      required_extra_info_v1_params = [company_info, action_plan_response[1][0], request_for_proposal, request_for_proposal]
      past_experience_v1_params = [company_info, action_plan_response[1][0], request_for_proposal, past_projects, request_for_proposal]

      timeline_response = await timeline_v1(timeline_v1_params)
      required_extra_info_response = await required_extra_info_v1(required_extra_info_v1_params)
      past_experience_response = await past_experience_v1(past_experience_v1_params)

      closing_v1_params = [request_for_proposal, company_info, action_plan_response[1][0], past_projects, past_experience_response[1][0], intro_response[1][0]]
      
      closing_response = await closing_v1(closing_v1_params)

      # Esperar las tareas restantes (si las hay)
      for task in tasks:
        result = await task
        collected_results.append(result)
      
      owner_name_response = collected_results[2]
      requirements_summary_response = collected_results[3]
      goals_response = collected_results[4]
      dates_response = collected_results[5]

      if not owner_name_response:
        # print("No se ha procesado owner_name_v1 y por lo tanto no se han obtenido respuestas")
        promps_notes.append("No se ha procesado owner_name_v1 y por lo tanto no se han obtenido respuestas")
    
      if not requirements_summary_response:
        # print("No se ha procesado requirements_summary_v1 y por lo tanto no se han obtenido respuestas")
        promps_notes.append("No se ha procesado requirements_summary_v1 y por lo tanto no se han obtenido respuestas")
      
      if not goals_response:
        # print("No se ha procesado goals_v1 y por lo tanto no se han obtenido respuestas")
        promps_notes.append("No se ha procesado goals_v1 y por lo tanto no se han obtenido respuestas")
      
      if not dates_response:
        # print("No se ha procesado dates_v1 y por lo tanto no se han obtenido respuestas")
        promps_notes.append("No se ha procesado dates_v1 y por lo tanto no se han obtenido respuestas")
      
      if not intro_response:
        # print("No se ha procesado intro_v1 y por lo tanto no se han obtenido respuestas")
        promps_notes.append("No se ha procesado intro_v1 y por lo tanto no se han obtenido respuestas")
        
      if not action_plan_response:
        # print("No se ha procesado action_plan_v1 y por lo tanto no se han obtenido respuestas")
        promps_notes.append("No se ha procesado action_plan_v1 y por lo tanto no se han obtenido respuestas")
      
      if not timeline_response:
        # print("No se ha procesado timeline_v1 y por lo tanto no se han obtenido respuestas")
        promps_notes.append("No se ha procesado timeline_v1 y por lo tanto no se han obtenido respuestas")
      
      if not required_extra_info_response:
        # print("No se ha procesado required_extra_info_v1 y por lo tanto no se han obtenido respuestas")
        promps_notes.append("No se ha procesado required_extra_info_v1 y por lo tanto no se han obtenido respuestas")

      if not past_experience_response:
        # print("No se ha procesado past_experience_v1 y por lo tanto no se han obtenido respuestas")
        promps_notes.append("No se ha procesado past_experience_v1 y por lo tanto no se han obtenido respuestas")
      
      if not closing_response:
        # print("No se ha procesado closing_v1 y por lo tanto no se han obtenido respuestas")
        promps_notes.append("No se ha procesado closing_v1 y por lo tanto no se han obtenido respuestas")
      
      # print("======================= INICIO RESPONSES =======================")
      # print("======================= owner_name_response =======================")
      # print("======================= ***** =======================")

      
      # print(owner_name_response)

      # print("======================= requirements_summary_response =======================")
      # print("======================= ***** =======================")
      # print("======================= ***** =======================")
      
      # print(requirements_summary_response)

      # print("======================= goals_response =======================")
      # print("======================= ***** =======================")
      # print("======================= ***** =======================")
      
      # print(goals_response)

      # print("======================= dates_response =======================")
      # print("======================= ***** =======================")
      # print("======================= ***** =======================")
      
      # print(dates_response)

      # print("======================= intro_response =======================")
      # print("======================= ***** =======================")
      # print("======================= ***** =======================")
      
      # print(intro_response)

      # print("======================= action_plan_response =======================")
      # print("======================= ***** =======================")
      # print("======================= ***** =======================")
      
      # print(action_plan_response)

      # print("======================= timeline_response =======================")
      # print("======================= ***** =======================")
      # print("======================= ***** =======================")
      
      # print(timeline_response)

      # print("======================= required_extra_info_response =======================")
      # print("======================= ***** =======================")
      # print("======================= ***** =======================")
      
      # print(required_extra_info_response)

      # print("======================= past_experience_response =======================")
      # print("======================= ***** =======================")
      # print("======================= ***** =======================")
      
      # print(past_experience_response)

      # print("======================= closing_response =======================")
      # print("======================= ***** =======================")
      # print("======================= ***** =======================")
      
      # print(closing_response)

      # print("======================= ***** =======================")
      # print("======================= ***** =======================")
      # print("======================= FIN RESPONSES =======================")

      # Guardar la respuesta en Supabase (OPCIONAL)
      owner_name_supabase_response = save_response_to_supabase(
        owner_name_response[0],
        owner_name_response[1][0],
        company_id,
        owner_name_response[1][1]["prompt_tokens"],
        owner_name_response[1][1]["completion_tokens"],
        proposal_id,
        owner_name_response[2] # prompt_id
      )
      requirements_summary_supabase_response = save_response_to_supabase(
        requirements_summary_response[0],
        requirements_summary_response[1][0],
        company_id,
        requirements_summary_response[1][1]["prompt_tokens"],
        requirements_summary_response[1][1]["completion_tokens"],
        proposal_id,
        requirements_summary_response[2] # prompt_id
      )
      goals_supabase_response = save_response_to_supabase(
        goals_response[0],
        goals_response[1][0],
        company_id,
        goals_response[1][1]["prompt_tokens"],
        goals_response[1][1]["completion_tokens"],
        proposal_id,
        goals_response[2] # prompt_id
      )
      dates_supabase_response = save_response_to_supabase(
        dates_response[0],
        dates_response[1][0],
        company_id,
        dates_response[1][1]["prompt_tokens"],
        dates_response[1][1]["completion_tokens"],
        proposal_id,
        dates_response[2] # prompt_id
      )
      intro_supabase_response = save_response_to_supabase(
        intro_response[0],
        intro_response[1][0],
        company_id,
        intro_response[1][1]["prompt_tokens"],
        intro_response[1][1]["completion_tokens"],
        proposal_id,
        intro_response[2] # prompt_id
      )
      action_plan_supabase_response = save_response_to_supabase(
        action_plan_response[0],
        action_plan_response[1][0],
        company_id,
        action_plan_response[1][1]["prompt_tokens"],
        action_plan_response[1][1]["completion_tokens"],
        proposal_id,
        action_plan_response[2] # prompt_id
      )
      timeline_supabase_response = save_response_to_supabase(
        timeline_response[0],
        timeline_response[1][0],
        company_id,
        timeline_response[1][1]["prompt_tokens"],
        timeline_response[1][1]["completion_tokens"],
        proposal_id,
        timeline_response[2] # prompt_id
      )
      required_extra_info_supabase_response = save_response_to_supabase(
        required_extra_info_response[0],
        required_extra_info_response[1][0],
        company_id,
        required_extra_info_response[1][1]["prompt_tokens"],
        required_extra_info_response[1][1]["completion_tokens"],
        proposal_id,
        required_extra_info_response[2] # prompt_id
      )
      past_experience_supabase_response = save_response_to_supabase(
        past_experience_response[0],
        past_experience_response[1][0],
        company_id,
        past_experience_response[1][1]["prompt_tokens"],
        past_experience_response[1][1]["completion_tokens"],
        proposal_id,
        past_experience_response[2] # prompt_id
      )
      closing_supabase_response = save_response_to_supabase(
        closing_response[0],
        closing_response[1][0],
        company_id,
        closing_response[1][1]["prompt_tokens"],
        closing_response[1][1]["completion_tokens"],
        proposal_id,
        closing_response[2] # prompt_id
      )

      concatenated_supabase_response = save_response_to_supabase(
        "Intro, Proposal, Closing",
        f"{intro_response[1][0]} {action_plan_response[1][0]} {closing_response[1][0]}",
        company_id,
        0,
        0,
        proposal_id,
        0 # prompt_id
      )
      
      proposal_content_processed = save_proposal_content(proposal_id, f"{intro_response[1][0]} {action_plan_response[1][0]} {closing_response[1][0]}")
      proposal_summary_processed = save_proposal_summary(proposal_id, requirements_summary_response[1][0])

      if not owner_name_supabase_response:
        supabase_notes.append("No se han guardado las respuestas de owner_name_v1 en la base de datos")
      
      if not requirements_summary_supabase_response:
        supabase_notes.append("No se han guardado las respuestas de requirements_summary_v1 en la base de datos")
      
      if not goals_supabase_response:
        supabase_notes.append("No se han guardado las respuestas de goals_v1 en la base de datos")
      
      if not dates_supabase_response:
        supabase_notes.append("No se han guardado las respuestas de dates_v1 en la base de datos")
      
      if not intro_supabase_response:
        supabase_notes.append("No se han guardado las respuestas de intro_v1 en la base de datos")
      
      if not action_plan_supabase_response:
        supabase_notes.append("No se han guardado las respuestas de action_plan_v1 en la base de datos")
      
      if not timeline_supabase_response:
        supabase_notes.append("No se han guardado las respuestas de timeline_v1 en la base de datos")

      if not required_extra_info_supabase_response:
        supabase_notes.append("No se han guardado las respuestas de required_extra_info_v1 en la base de datos")

      if not past_experience_supabase_response:
        supabase_notes.append("No se han guardado las respuestas de past_experience_v1 en la base de datos")

      if not closing_supabase_response:
        supabase_notes.append("No se han guardado las respuestas de closing_v1 en la base de datos")

      if not concatenated_supabase_response:
        supabase_notes.append("No se han guardado las respuestas de informe concatenado en la base de datos")
      
      # print("PROCESS FINISHED")

      if len(promps_notes) > 0 or len(supabase_notes) > 0:
        print(promps_notes)
        print(supabase_notes)
        return JsonResponse({"error": "Error al guardar la respuesta en la base de datos"}, status=500)
      else:
        return JsonResponse({"message": "Respuesta procesada y guardada exitosamente"}, safe=False)

    # owner_name_response = await owner_name_v1(owner_name_v1_params)
    # requirements_summary_response = await requirements_summary_v1(requirements_summary_v1_params)
    # goals_response = await goals_v1(goals_v1_params)
    # dates_response = await dates_v1(dates_v1_params)
    # intro_response = await intro_v1(intro_v1_params)
    # action_plan_response = await action_plan_v1(action_plan_v1_params)

    #if not owner_name_response:
      #return JsonResponse({"message": "Error al procesar el prompt. Verifique el número de parámetros o llamadas externas."}, safe=False)
  except NameError:
    # print(NameError)
    return JsonResponse({"error": "Error al procesar la solicitud en el servidor"}, status=500)

# @csrf_protect
# @api_view(['POST'])
@csrf_exempt
def verify_firebase_token(request):
  token = request.headers.get('Authorization').split(' ').pop()
  try:
    decoded_token = auth.verify_id_token(token)
    uid = decoded_token['uid']
    return JsonResponse({'message': 'Token verificado', 'uid': uid})
  except:
    return JsonResponse({'error': 'Token inválido'}, status=401)

# @api_view(['POST'])
@csrf_exempt
def create_new_firebase_user(request):
  request_body = json.loads(request.body.decode('utf-8'))

  new_email = request_body['email']
  new_password = request_body['password']
  new_display_name = request_body['display_name']

  try:
    user = auth.create_user(
      email = new_email,
      email_verified = False,
      password = new_password,
      display_name = new_display_name,
      disabled = False
    )

    user_data = {
      "uid": user.uid,
      "email": user.email,
      "display_name": user.display_name,
      "email_verified": user.email_verified,
      "disabled": user.disabled,
      # Añade otros campos relevantes que quieras devolver
    }

    return JsonResponse({'message': 'Usuario creado', 'user': user_data})
  except Exception as error:
    # print(error)
    return JsonResponse({'error': 'Error al crear el usuario'}, status=401)

# @api_view(['GET'])
@csrf_exempt
def get_user_by_email(request):
  try:
    user_email = request.GET.get('user_email')

    user = auth.get_user_by_email(user_email)
    
    return JsonResponse({'message': 'Usuario obtenido', 'user': user.uid})
  except:
    return JsonResponse({'error': 'Error al obtener el usuario'}, status=401)

# @api_view(['PUT'])
@csrf_exempt
def update_firebase_user(request):
  request_body = json.loads(request.body.decode('utf-8'))

  user_uid = request_body['user_uid']
  new_email = request_body['email']
  new_password = request_body['password']
  new_display_name = request_body['display_name']

  try:
    auth.update_user(
      user_uid,
      email = new_email,
      password = new_password,
      display_name = new_display_name
    )
    return JsonResponse({'message': 'Usuario actualizado', 'user': user_uid})
  except:
    return JsonResponse({'error': 'Error al actualizar el usuario'}, status=401)

# @api_view(['DELETE'])
@csrf_exempt
def delete_firebase_user(request):
  user_uid = request.GET.get('user_uid')
  try:
    auth.delete_user(user_uid)
    return JsonResponse({'message': 'Usuario eliminado', 'user': user_uid})
  except:
    return JsonResponse({'error': 'Error al eliminar el usuario'}, status=401)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": "This is a protected view."})

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
def weaviate_connection():
  client = weaviate.Client(
     url = "https://o8rdynkss2uddb4ldicfsg.c0.us-central1.gcp.weaviate.cloud",  # Replace with your endpoint
     auth_client_secret=weaviate.AuthApiKey(config('api_key_weaviate')),  # Replace w/ your Weaviate instance API key
     additional_headers = {
         "X-OpenAI-Api-Key": config('OPENAI_APIKEY')  # Replace with your inference API key
     }
  )


  return client

def create_db_connection():
  """
  Creates and returns a connection to the PostgreSQL database.
  
  Returns:
  psycopg2.connection: A connection object to the PostgreSQL database.
  """
  DB_HOST = config('DB_HOST')
  DB_NAME = config('DB_NAME')
  DB_USER = config('DB_USER')
  DB_PASSWORD = config('DB_PW')

  try:
      conn = psycopg2.connect(
          host=DB_HOST,
          dbname=DB_NAME,
          user=DB_USER,
          password=DB_PASSWORD
      )
      return conn
  except Exception as e:
      return JsonResponse({"status": "error", "message": str(e)})

def create_class_weaviate(request):
  client = weaviate_connection()

  if client.schema.exists("TestingConn"):
    client.schema.delete_class("TestingConn")
  class_obj = {
      "class": "TestingConn",
      "vectorizer": "text2vec-openai",  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
      "moduleConfig": {
          "text2vec-openai": {},
          "generative-openai": {}  # Ensure the `generative-openai` module is used for generative queries
      }
  }

  client.schema.create_class(class_obj)
  return HttpResponse(200)

def get_collections(request):
  client = weaviate_connection()
  schema = client.schema.get()
  return JsonResponse(schema)

def execute_queries(request):
  """
  Executes specific database queries and returns the results.

  Args:
  request: HttpRequest object

  Returns:
  JsonResponse: A JSON response containing the query results.
  """
  conn = create_db_connection()
  if conn is None or conn.closed:
      return JsonResponse({"status": "error", "message": "Database connection is not available"})

  try:
      cur = conn.cursor()
      # Execute queries
      cur.execute("SELECT * FROM Proposals")
      proposals = cur.fetchall()
      proposals_columns = [desc[0] for desc in cur.description]
      proposals_data = [dict(zip(proposals_columns, row)) for row in proposals]

      cur.execute("SELECT * FROM public.requests_for_proposals")
      rfps = cur.fetchall()
      rfps_columns = [desc[0] for desc in cur.description]
      rfps_data = [dict(zip(rfps_columns, row)) for row in rfps]

      # Return the results
      return JsonResponse({
          "status": "success",
          "proposals": proposals_data,
          "requests_for_proposals": rfps_data
      })
  except Exception as e:
      return JsonResponse({"status": "error", "message": str(e)})
  finally:
      cur.close()  
   


def bid_slice_text(request, text):
  class Document:
    def __init__(self, content, metadata={}):
        self.page_content = content
        self.metadata = metadata

  def slice_text(documents, chunk_overlap=0, separators=["\n\n", "\n", "(?<=\. )", " "]):
    text_splitter = RecursiveCharacterTextSplitter(
        #chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=separators,
        length_function=len
    )
    return text_splitter.split_documents(documents)

  # Create a Document instance with your dummy text
  text = """
    REQUESTS FOR PROPOSALS COMMUNICATIONS CONSULTING SERVICES
    I. GENERAL INFORMATION
    A. INTRODUCTION
    The Intergovernmental Personnel Benefit Cooperative (IPBC) is seeking proposals from
    qualified individuals or firms to provide communications consulting services for the
    IPBC. Successful applicants will demonstrate an ability to provide: provide a
    comprehensive analysis of IPBC’s communication structure and recommendation for a
    future state.
    B. BACKGROUND
    IPBC is a partnership of local government entities in Illinois that are committed to the
    philosophy of risk pooling and working together to provide cost-effective health and
    related employee benefits. Formed in 1979, IPBC has grown from 8 members to over
    160. It is open to municipalities, counties, special agencies, and intergovernmental
    organizations.
    IPBC is staffed by four (4) full-time staff members and one (1) part-time staff member.
    IPBC contracts with Risk Program Administrators (RPA) to provide benefit consulting
    services to the membership. RPA is currently staffed by ten (10) full-time staff members.
    IPBC provides health (BCBSIL, UHC), life (Securian), dental (DDIL), vision (VSP), and
    spending account (WEX) benefits for its membership. In addition, IPBC utilizes
    PlanSource as the benefits administration platform.
    IPBC communicates with its member entities who then are responsible for
    communicating their benefit programs with their employees. IPBC communicates with
    its members via:
    • Monthly Newsletter (Attachment A)
    • E-mail Blasts (Attachment B)
    • Governance Meetings – held quarterly, open to entire membership (Attachment
    C)
    • IPBC Website: [www.ipbchealth.org](http://www.ipbchealth.org/) – each member is given a login. The website
    contains information that is applicable to entire membership (financial reports,
    meeting packets, carrier flyers). The website does not have the ability to easily
    share/store member specific documents/information with the member entities.
    A quick video overview of the website is available here:
    https://vimeo.com/manage/videos/888761301
    • Individual communications between IPBC and benefit consultants via e-mail and
    phone.
    IPBC member entities are responsible for communicating their individual benefits
    program(s) to their employees. It is at the discretion of the member entities on how they
    communicate with their employees (i.e, email, intranet, employer newsletters etc.) In
    addition, IPBC carrier partners communicate directly with employees on their services.
    C. ANTICIPATED SELECTION SCHEDULE
    IPBC anticipates the following general timeline for its selection process. The IPBC
    reserves the right to change this schedule.
    • RFP Advertised Week of November 27, 2023
    • Proposal Due Date (post marked by) December 20, 2023 by 5:00 pm
    • Evaluation of Proposals Weel of January 8, 2024
    • Interviews (if needed) Week of January 29, 2024
    • Contract Approval March 2024 (Board Meeting)
    • Commencement of Contract July 1, 2024
    D. SCOPE OF SERVICES
    The scope of work will include the following tasks:
    Development of a Communications Plan for IPBC, which should include coordination with
    the IPBC Staff and the IPBC Membership Development Committee on both planning and
    implementation.
    Creation/recommendation of the necessary infrastructure, such as websites or other
    communications tools, to enable plan implementation to begin, and support for
    implementation of the approved communications plan during the initial 6-12 months. This
    may include, but not be limited to:
     Conducting an Inventory of all current communication materials
     Coordinating the communication strategies with IPBC Staff and the
    Membership Development Committee,
     Producing creative materials and building/recommending the necessary
    dissemination infrastructure,
     Writing articles, marketing pieces, information releases,
    Primary Audience
    The primary audience is Human Resources and Finance staff of local government agencies
    who are responsible for managing their entity’s benefit program(s). The secondary
    audience are the employees who are participating in an IPBC benefit program.
    Anticipated Contract Type
    IPBC would expect to negotiate a firm fixed fee and enter into a contract for
    communications service(s) selected through this RFP. This contract is expected to have a
    duration of 18-24 months, depending upon the length of the Task 1 planning phase and the
    activities subsequently agreed upon for future phases. The contract may be renewed,
    based upon performance and need.
    II. PROPOSAL INSTRUCTIONS
    A. PROPOSAL SUBMITTAL AND DUE DATE
    Proposers shall provide proposal electronically marked “IPBC Communications Services
    Proposal”. Proposals shall be submitted by 5:00 p.m. on XX to:
    Sandy Mikel
    Member Services Manager
    [smikel@ipbchealth.org](mailto:smikel@ipbchealth.org)
    B. INQUIRIES
    Questions concerning this RFP should be submitted to:
    Sandy Mikel
    Member Services Manager
    [smikel@ipbchealth.org](mailto:smikel@ipbchealth.org)
    IPBC will not respond to questions received after 3:00p.m. on December 20, 2023.
    C. RESERVATION OF RIGHTS
    IPBC reserves the right to: 1) seek clarifications of each proposal; 2) negotiate a final
    contract that is in the best interest of the IPBC and its membership; 3) reject any or all
    proposals; 4) cancel this RFP at any time if doing so would be in the membership’s
    interest, as determined by IPBC in its sole discretion; 5) award the contract to any
    proposer based on the evaluation criteria set forth in this RFP; 6) waive minor informalities
    contained in any proposal, when, in the IPBC’s sole judgment, it is in the IPBC’s best
    interest to do so; and 7) request any additional information IPBC deems reasonably
    necessary to allow IPBC to evaluate, rank and select the most qualified Proposer to
    perform the services described in this RFP.
    D. PROPOSAL CONTENTS
    Proposals shall include, at a minimum, the following items:
    - Cover Letter. A one page cover letter containing:
    * the name of the person(s) authorized to represent the Proposer
    in negotiating and signing any agreement which may result from the
    proposal;
    * Entity name and address;
    * Phone, website and email address; and
    - Staffing. Name and qualifications of the individuals who will provide the requested
    services and a current résumé for each, including a description of qualifications,
    skills, and responsibilities. The IPBC is interested in professionals with experience
    serving governmental entities and membership organizations comparable to IPBC.
    - Approach/Work Plan. Describe how the Proposer approaches marketing and
    communications projects. How do you assist clients in using existing resources and
    leveraging the work you provide for them?
    - Experience/Work Samples. Provide previous work examples that demonstrate how
    you meet the experience requirements listed in this RFP. Submit three projects
    undertaken in the past three years (preferably for a membership organization
    similar to in structure to IPBC)
    - Cost/Budget. Provide hourly rates or other fee structures for the services listed in
    Article 1.E, Scope of Services, of this RFP.
    - Capacity. Explain proposer’s workload capacity and level of
    experience commensurate with the level of service required by IPBC.
    - Insurance. Proof of Insurance of $2 million comprehensive and automobile liability
    insurance, as well as proof of coverage by Workers’ Compensation Insurance or
    exemption.
    - Subconsultants. A list of the tasks, responsibilities, and qualifications of any
    subconsultants proposed to be used on a routine basis.
    - Nondiscrimination. Written affirmation that the firm has a policy of
    nondiscrimination in employment because of race, age, color, sex, religion, national
    origin, mental or physical handicap, political affiliation, marital status or other
    protected class, and has a drug-free workplace policy.
    E. INFORMATION RELEASE
    Proposers are hereby advised that IPBC may solicit background information based upon
    all information, including references, provided in response to this RFP. By submission of
    a proposal, Proposer agrees to such activity and releases IPBC from all claims arising
    from such activity.
    F. PUBLIC RECORDS
    All proposals submitted are the property of IPBC, and are thus subject to disclosure
    pursuant to the public records law.
    Proposers responding to this RFP do so solely at their own expense.
    III. PROPOSAL EVALUATION
    A. MINIMUM QUALIFICATIONS
    The IPBC will review proposals received to determine whether or not each proposer
    meets the following minimum qualifications:
    • Ability to provide the marketing and communications services work needed by
    the IPBC to the standards required by the IPBC.
    • Has the financial resources for the performance of the desired marketing and
    communication services, or the ability to obtain such resources.
    • Is an Equal Opportunity Employer and otherwise qualified by law to enter into the
    attached Marketing and Communications Services Contract.
    B. EVALUATION CRITERIA
    If an award is made, it is expected that the IPBC’s award will be to the applicant that agrees
    to meet the needs of the IPBC. A number of relevant matters will be considered, including:
    1. Experience in the development of communications plans of similar purpose and
    scope
    2. Demonstrated effectiveness in the implementation of a variety of communications
    tactics that achieve established goals
    3. Understanding of and approach to the listed scope of services
    4. Cost proposal
    Interviews may be requested prior to final selection.
    C. SELECTION
    An evaluation committee will evaluate all proposals. The committee will be composed of
    IPBC Staff, Benefit Consulting Staff and members of the IPBC Membership Development
    Committee.
    Upon completion of its evaluation process, the evaluation committee shall provide the
    results of the scoring and ranking to the IPBC Board of Directors, along with a
    recommendation to award the contract to the highest ranked Proposer.
    D. CONTRACT
    IPBC desires to enter into a professional services agreement, which includes all necessary
    marketing and communications services, whether or not the services are specifically
    outlined in this RFP. The agreement requires that awardee comply with all applicable
    federal and state laws, rules and regulations
    IPBC is an Equal Opportunity/Affirmative Action Employer. Women,
    Minorities, and Disabled Persons are encouraged to apply.
    THIS SOLICITATION IS NOT AN IMPLIED CONTRACT AND MAY BE
    MODIFIED OR REVOKED WITHOUT NOTICE.
  """
  data = Document(text)
  
  # Slicing the dummy text
  sliced_docs = slice_text([data])
  slice_output = []
  length_of_sliced_docs = len(sliced_docs)

  for i, doc in enumerate(sliced_docs):
    document_object = {
      "contect" : doc.page_content,
      "part_number" : i
    }

    slice_output.append(document_object)

  final_output = json.dumps(slice_output, indent = 4)

  return JsonResponse(final_output, safe=False)

# @api_view(['GET'])
def unprotected_view(request):
    return HttpResponse(f'<h1>Welcome to Bidline Services</h1>')
