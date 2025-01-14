from jira import JIRA, JIRAError
from jira.resources import Comment
import requests
import os
import re
import keyboard


#Путь к файлу
with open("UpdatePatient.txt", 'w', encoding="utf-8") as foi:

    #Подключение и аутентификация
    authData123 = open("creds.txt", 'r')
    authDataRead = authData123.read()

    jira_address = "https://jira.mos.social"

    jira_user = authDataRead.split('LOGIN:')[1]
    jira_user = jira_user.split('\nPASSWORD:')[0]

    jira_password = authDataRead.split('PASSWORD:')[1]
    jira_password = jira_password.split('\nEPIC:')[0]

    jira_epic = authDataRead.split('EPIC:')[1]
    jira = JIRA(server=jira_address, basic_auth=(jira_user, jira_password))

    # Получение списка задач
    jqlRequest = 'project = COVIDVAC AND resolution = Unresolved AND text ~ "сверить данные" AND assignee in (currentUser()) ORDER BY key ASC, priority DESC, updated DESC'
    listOfJiraIssues = jira.search_issues(jqlRequest)


    #Получение данных из задачи
    patternOldPatient = 'старые patient_id:'
    patternOldPatientOne = 'старый patient_id:'
    patternNewPatient = 'новые patient_id:'
    patternNewPatientOne = 'новый patient_id:'

    #Функция поиска старых id
    def findOldId():
        if patternOldPatient in descOld:
            oldId = descOld.split('старые patient_id:')[1]
            oldId = oldId.split('\n')[0]
            oldId = ''.join(re.findall(r'\d', oldId))
        elif patternOldPatientOne in descOld:
            oldId = descOld.split('старый patient_id:')[1]
            oldId = oldId.split('\r')[0]
            oldId = ''.join(re.findall(r'\d', oldId))
        return oldId

    #Функция поиска новых id
    def findNewId():
        if patternNewPatient in descNew:
            newId = descNew.split('новые patient_id:')[1]
            newId = newId.split('\n')[0]
            newId = ''.join(re.findall(r'\d', newId))
        elif patternNewPatientOne in descNew:
            newId = descNew.split('новый patient_id:')[1]
            newId = newId.split('\r')[0]
            newId = ''.join(re.findall(r'\d', newId))
        return newId

    #Поиск patient_id в задачах и формирование sql-запроса
    for issue in listOfJiraIssues:
        if issue:
            key = issue.key
            descOld = issue.fields.description
            descNew = issue.fields.description
            oldId = findOldId()
            newId = findNewId()
            foi.write(f"--{key}\n"
                                 f"update covid_vaccination set patient_erp_id = '{newId}' where patient_erp_id = '{oldId}';\n"
                                 f"update inspection set patient_erp_id = '{newId}' where patient_erp_id = '{oldId}';\n"
                                 f"update doc_transfer_egisz set patient_erp_id = '{newId}' where patient_erp_id = '{oldId}';\n"
                                 f"\n")

            print(f"Данные перенесены с {oldId} на {newId} в задаче {key}")

print('Нажмите ENTER для выхода...')
keyboard.read_event('enter')


