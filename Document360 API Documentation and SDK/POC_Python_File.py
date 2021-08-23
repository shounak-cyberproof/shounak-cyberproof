#!/usr/bin/env python
# coding: utf-8

# # POC for Document360 API
# 
# ## POC coverage:
# * Getting Project Details, Categories, Articles
# * Checking, Creating & Deleting Users
# * Deleting and Creating Categories
# * Deleting, Creating & Publishing Articles
# * Creating Readers and Reader Group
# 
# 
# #### Note:
# The sleep time is used to prevent the API calls from exceeding the API call limit for the trial version of Document360 which leads to immediate blocking of the trial account

# In[1]:


import requests
from time import sleep
"""From api_resource, we will be importing classes which will hlp us make the API calls"""
from api_resource import (
    Project_Api,
    Teams,
    Category,
    Article,
    Misc_Articles,
    Bulk_Articles,
    Reader,
    Reader_Group,
)
import json
import warnings
warnings.filterwarnings("ignore")


"""API tokens"""
# for trial account, API token gets deleted over time. 
# During testing the POC, request the viewer to create a new Trial Account and use that account's token
private_api_token = "C914tZyYDm2o2ncWE6uf6oHgcg0y3+FOWBY7qmLZcDOF98qn+Fnn2ty9BW+6EN1WrsfkySn2xjExJvLJiIkweiAGgXFubusdoKTJZgRuwh9VkirucZT134LXgx8aszfRL6s0W/0hP8MGw1q8D9nAHA=="


"""base url"""
base_url = "https://apihub.document360.io/v1/"


"""defining headers"""
private_headers = {"api_token": private_api_token, "Content-Type": "application/json"}


"""creating objects"""
prv_proj_obj = Project_Api(base_url=base_url, headers=private_headers)
prv_teams_obj = Teams(base_url=base_url, headers=private_headers)
prv_category_obj = Category(base_url=base_url, headers=private_headers)
prv_article_obj = Article(base_url=base_url, headers=private_headers)
prv_misc_articles_obj = Misc_Articles(base_url=base_url, headers=private_headers)
prv_bulk_articles_obj = Bulk_Articles(base_url=base_url, headers=private_headers)
prv_reader_obj = Reader(base_url=base_url, headers=private_headers)
prv_reader_group_obj = Reader_Group(base_url=base_url, headers=private_headers)


# ### Start screen of the Private Project
# <img src="images/1_start.png">
# 
# By default, Document360 starts with below Categories and articles in them:
# * Getting started
# * Home page builder
# * Drive
# * Analytics
# * Settings

# In[2]:


"""First, let us delete all articles so we can start fresh"""

# private project ID (required for getting list of articles)
prv_project_id = prv_proj_obj.get_project_id()

sleep(1)

# getting list of articles
article_id_list_prv = prv_proj_obj.get_article_ID_list()

sleep(1)

"""We will delete first 4 articles"""

bulk_delete_parameters = {"article_ids": article_id_list_prv.values()}
print(prv_bulk_articles_obj.delete_bulk_articles(bulk_delete_parameters))

sleep(1)


# In[7]:


"""We will then delete all Categories"""
category_id_list_prv = prv_proj_obj.get_category_ID_list()

"""since bulk delete option is not available for Categories, we will delete one by one via loop"""
for cat_id in category_id_list_prv.values():
    print(prv_category_obj.delete_category(cat_id))
    sleep(2)


# ### Screen after deleting the Articles and Categories
# 
# <img src="images/2_deleted_cat.png">

# In[8]:


"""Now that we have a clean slate, let us add Categories to our Project"""
add_cat_prv_parameters_1 = {
    "name": "English Premier League",
    "project_version_id": prv_project_id,
}
prv_category_obj.post_add_category(add_cat_prv_parameters_1)

sleep(1)

add_cat_prv_parameters_2 = {"name": "La Liga", "project_version_id": prv_project_id}
prv_category_obj.post_add_category(add_cat_prv_parameters_2)

sleep(1)

add_cat_prv_parameters_3 = {"name": "Serie A", "project_version_id": prv_project_id}
prv_category_obj.post_add_category(add_cat_prv_parameters_3)

sleep(1)

add_cat_prv_parameters_4 = {"name": "Bundesliga", "project_version_id": prv_project_id}
prv_category_obj.post_add_category(add_cat_prv_parameters_4)

sleep(1)


# In[9]:


"""Get list of new Category IDs"""
category_id_list_prv = prv_proj_obj.get_category_ID_list()


# In[17]:


"""Add Articles in the Categories"""
user_id = prv_teams_obj.primary_user_id()

sleep(1)

parameters = [
    {
        "title": "Teams in EPL",
        "category_id": list(category_id_list_prv.values())[0],
        "project_version_id": prv_project_id,
        "user_id": user_id,
        "content": "#Top Teams in EPL are <br> Man City, Man Utd, Chelsea, Liverpool",
    },
    {
        "title": "Teams in La Liga",
        "category_id": list(category_id_list_prv.values())[1],
        "project_version_id": prv_project_id,
        "user_id": user_id,
        "content": "#Top Teams in La Liga are <br> Real Madrid, Atletico Madrid, Barcelona, Villarreal",
    },
]

print(prv_bulk_articles_obj.post_bulk_add_articles(parameters=parameters))

sleep(1)


# ## After adding the Categories and Articles, the Project Page appears as below:
# <img src="images/3_posted_articles.png">
# 
# ## On Website, the documentation appears as below:
# ### Note: Only published items will be visible on Website
# <img src="images/4_website_docs.png">

# In[20]:


"""List of new Categories & Articles inside it"""

cat_id_dict = prv_proj_obj.get_category_ID_list()

for cat_id in list(cat_id_dict.values()):
    print(prv_category_obj.get_category(cat_id))

sleep(1)


# In[21]:


sleep(1)

article_id_list_prv = prv_proj_obj.get_article_ID_list()


# In[23]:


"""To publish articles on web, we can make the below API call. We will be using bulk upload option"""
params = []
for art_id in article_id_list_prv:
    params.append({"article_id" : art_id, "version_number": 1, "user_id": user_id})

print(prv_bulk_articles_obj.post_bulk_publish_articles(parameters=params))
sleep(5)


# ## To Check Users in System & Add New Users

# In[24]:


"""Check current users"""
print(prv_teams_obj.get_users())


# In[25]:


"""Adding a user with user_role as editor"""

parameters = {
    "email_id": "mark.noble@email.com",
    "user_role": 2,
    "user_id": user_id,
    "is_sso_user": False,
}

sleep(1)

print(prv_teams_obj.post_add_user(parameters=parameters))


# ## Added User is visible in Team & Security of Project Dashboard
# <img src="images/5_users.png">

# In[26]:


"""Adding a user with user_role as 'reader' """

parameters = {
    "email_id": "codabo6388@asmm5.com",
    "user_role": 4,
    "user_id": user_id,
    "is_sso_user": False,
}

sleep(1)

print(prv_teams_obj.post_add_user(parameters=parameters))


# In[27]:


"""Recheck current users after addition"""
print(prv_teams_obj.get_users())

sleep(1)


# ## To Create Readers (Applicable only in case of Private Projects)
# Only created readers will be able to see the Documentation

# In[28]:


"""Check existing readers (Earlier we added codabo6388@asmm5.com as 'reader')"""
print(prv_reader_obj.get_readers())

sleep(1)


# In[29]:


"""Adding new readers"""

email_list = ["bacaxa4582@cytsl.com","rarkadusti@biyac.com"]

for email in email_list:
    parameters = {"email_id": email}
    print(prv_reader_obj.post_add_reader(parameters))
    sleep(2)


# In[30]:


"""Checking updated reader list"""
print(prv_reader_obj.get_readers())


# ## Creation of Reader Group

# In[31]:


"""Creating 3 categories for Content_Writer, Software_Engineers, Owner"""

parameters_cw = {
    "name": "Content Writer Category",
    "project_version_id": prv_project_id,    
    "content": "# This category is for the Content Writer <br> ### This is the body of the page",
    "category_type": 1,
    "user_id": user_id,
}
prv_category_obj.post_add_category(parameters_cw)
sleep(2)

parameters_se = {
    "name": "Software Engineer Category",
    "project_version_id": prv_project_id,
    "content": "# This category is for the SE <br> ### This is the body of the page",
    "category_type": 1,
    "user_id": user_id,
}
prv_category_obj.post_add_category(parameters_se)
sleep(2)


# In[34]:


"""Checking the updated Category ID list"""
cat_id_dict = prv_proj_obj.get_category_ID_list()
cat_id_dict


# In[35]:


"""Adding Articles"""
parameters = [
    {
        "title": "Content Writer Article",
        "category_id": cat_id_dict["Content Writer Category"],
        "project_version_id": prv_project_id,
        "user_id": user_id,
        "content": "# Content Writer Article <br> Enter the body of the content here",
    },
    {
        "title": "Software Engineer Article",
        "category_id": cat_id_dict["Software Engineer Category"],
        "project_version_id": prv_project_id,
        "user_id": user_id,
        "content": "# SE Article <br> Enter the body of the content here",
    },
]
print(prv_bulk_articles_obj.post_bulk_add_articles(parameters))
sleep(2)


# In[36]:


"""Get article IDs"""
art_id_dict = prv_proj_obj.get_article_ID_list()
print(art_id_dict)


# In[37]:


"""Pulishing Articles"""
sleep(2)
params = []
for article in art_id_dict.values():
    params.append({"article_id" : article, "version_number": 1, "user_id": user_id})

print(prv_bulk_articles_obj.post_bulk_publish_articles(parameters=params))


# In[41]:


"""Creating Reader Groups"""

access_scope_g1 = {
    "access_level": 1,
    "categories": [
cat_id_dict["Content Writer Category"]
    ]
}

parameters_g1 = {
    # MANDATORY_PARAMETER
    "title": "Content Writer Group",
    # OPTIONAL_PARAMETER
    "description": "Group for Content Writer",
    "associated_readers":["9a634e59-aa53-42d5-b082-1d9ab74c9997", "0c462671-19fa-42f1-93ef-8658d5760c33"],
    "access_scope": access_scope_g1,
}

print(prv_reader_group_obj.post_add_group(parameters_g1))
sleep(5)

access_scope_g2 = {
    "access_level": 1,
    "categories": [
cat_id_dict["Software Engineer Category"]
    ]
}

parameters_g2 = {
    # MANDATORY_PARAMETER
    "title": "Software Engineer Group",
    # OPTIONAL_PARAMETER
    "description": "Group for Software Engineer",
    "associated_readers":["392d9f7d-272d-4a7b-abb4-d2fd4b76dab5","f4ddd4f6-4e5f-4da0-946d-24729b575b49"],
    "access_scope": access_scope_g2,
}

print(prv_reader_group_obj.post_add_group(parameters_g2))

