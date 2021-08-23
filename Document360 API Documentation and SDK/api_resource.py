import requests
import json


class Project_Api:
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

    def get_project_versions(self):
        """this method returns the details of the project version"""
        response = requests.get(self.base_url + "projectversions", headers=self.headers, verify=False)
        return response.json(), response.status_code

    def get_project_id(self):
        """returns project version ID"""
        return Project_Api.get_project_versions(self)[0]["data"][0]["id"]

    def get_article_list(self, id):
        '''this method returns list of articles inside a project upon inserting the project ID.'''
        response = requests.get(self.base_url + f"projectversions/{id}/articles", headers=self.headers, verify=False)
        return response.json(), response.status_code

    def get_article_ID_list(self):
        """returns the Article IDs in the Project"""
        project_id = Project_Api.get_project_id(self)
        raw_data = Project_Api.get_article_list(self,project_id)[0]["data"]
        art_num = len(raw_data)
        art_dict = {raw_data[i]["title"]: raw_data[i]["id"] for i in range(art_num)}
        return art_dict

    def get_category_list(self, id):
        '''this method returns list of categories inside a project upon inserting the project ID.'''
        response = requests.get(self.base_url + f"projectversions/{id}/categories", headers=self.headers, verify=False)
        return response.json(), response.status_code

    def get_category_ID_list(self):
        """returns the Category IDs in the Project"""
        project_id = Project_Api.get_project_id(self)
        raw_data = Project_Api.get_category_list(self, project_id)[0]["data"]
        cat_num = len(raw_data)
        cat_dict = {raw_data[i]["name"]: raw_data[i]["id"] for i in range(cat_num)}
        return cat_dict

    def search_phrase(self, id, phrase):
        '''this method searches for a phrase inside project version in given language'''
        parameters = {"search_query": phrase}
        response = requests.get(self.base_url + f"projectversions/{id}/en", headers=self.headers, params=parameters,
                                verify=False)
        return response.json(), response.status_code

    def post_export_doc(self, parameters):
        """
            Start a new export. Returns export ID and status of export.

            parameters needs to be passed in format as below:
            parameters = {
                # MANDATORY_PARAMETERS
                      "entity":"<Area to export. It can be Project/Version/Category/Article>",
                      "entity_ids":"<id's of the given entity for other entities except Project>",
                # OPTIONAL_PARAMETERS
                      "filter_by_article_modified_at":"filter articles by modified at date range",
                      "exclude_media_files":"Exclude media files if its not needed"
                         }
        """
        response = requests.post(self.base_url + "project/export", headers=self.headers, data=json.dumps(parameters),
                                 verify=False)
        return response.json(), response.status_code

    def get_export_status(self, exportId):
        """Get current status of the export. URL is shared once
           exporting is complete which enables download of .zip file"""
        response = requests.get(self.base_url + f"project/export/{exportId}", headers=self.headers, verify=False)
        return response.json(), response.status_code

    def post_import_doc(self, parameters):
        """Import documentation from source documentation URL.

            parameters needs to be passed in format as below:
                parameters = {
                                "source_documentation_url": "<Source documentation zip URL and the file format should
                                                              be satisfied by Document360 standard. The max file size
                                                              should be less than 1GB>",
                                "publish_article": "<Import article and publish>",
                                "import_by": "Document360 user id"
                             }
        """

        response = requests.post(self.base_url + "project/import", headers=self.headers, data=json.dumps(parameters),
                                 verify=False)
        return response.json(), response.status_code

    def get_import_status(self, importId):
        """Get current status of the import"""
        response = requests.get(self.base_url + f"project/export/{importId}", headers=self.headers, verify=False)
        return response.json(), response.status_code


class Teams:
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

    def get_users(self, parameters=None):
        '''parameter needs to be passed in format as below:
           parameters = {"email_id": "<specify an email of the user to fetch>",
                         "role_id": "<1 - Administrator, 2 - Editor, 3 - DraftWriter, 4 - Reader, 7 - Owner>",
                         "IsSsoUser": "<Specify if user is Single Sign-On user or not>"}
                      '''

        response = requests.get(self.base_url + "teams", headers=self.headers, params=parameters, verify=False)
        return response.json(), response.status_code

    def get_one_user(self, id):
        """id is the id of the user"""
        response = requests.get(self.base_url + f"teams/{id}", headers=self.headers, verify=False)
        return response.json(), response.status_code

    def primary_user_id(self):
        """to be used only when no additional users are created"""
        return Teams.get_users(self)[0]["data"][0]["id"]

    def post_add_user(self, parameters):
        '''parameter needs to be passed in format as below:
           parameters = {"email_id": "<Email address of the new user>",
                         "user_role": "<1 - Administrator, 2 - Editor, 3 - DraftWriter, 4 - Reader, 7 - Owner>",
                         "user_id": "<The ID of the user that will be marked as an inviter>",
                         "is_sso_user": "<Specify if user is Single Sign-On user or not>"}
                         '''
        response = requests.post(self.base_url + "teams", headers=self.headers, data=json.dumps(parameters),
                                 verify=False)
        return response.json(), response.status_code

    def put_update_user_role(self, id, parameters):
        '''parameter needs to be passed in format as below. Enter the number:
           parameters = {"user_role": "<1 - Administrator, 2 - Editor, 3 - DraftWriter, 4 - Reader, 7 - Owner>"}
           '''
        response = requests.put(self.base_url + f"teams/{id}/role", headers=self.headers, params=parameters,
                                verify=False)
        return response.json(), response.status_code

    def delete_user(self, id):
        response = requests.delete(self.base_url + f"teams/{id}", headers=self.headers, verify=False)
        return response.json(), response.status_code

    def get_email_exists(self, parameters):
        '''parameter needs to be passed in format as below. Enter the number:
           parameters = {"email_id": "<email to be checked>"}
           '''
        response = requests.get(self.base_url + "teams/email-exists", headers=self.headers, params=parameters,
                                verify=False)
        return response.json(), response.status_code

    def get_team_roles(self):
        '''returns the id, role, description & hierarchy of the team members'''
        response = requests.get(self.base_url + "teams/roles", headers=self.headers, verify=False)
        return response.json(), response.status_code

    def get_IP_restrictions(self):
        '''returns the IP address restrictions'''
        response = requests.get(self.base_url + "teams/get-ip-address-restriction", headers=self.headers, verify=False)
        return response.json(), response.status_code

    def put_update_IP_restrictions(self, parameters):
        '''updates the IP address restrictions
           parameter needs to be passed in format as below:
           parameters:
        parameters = {"name": "<Name of the IP Restriction>",
                      "ip_address": "<IP Address range>",
                      "consider_for_restriction": "<Status of the IP Restriction (True or False)>",
                      "allow_or_block_ip_address": "<Allow or Block>"}'''
        response = requests.put(self.base_url + "teams/manage-ip-address", headers=self.headers, params=parameters,
                                verify=False)
        return response.json(), response.status_code


class Category:
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

    def get_category(self, id):
        '''returns category as per category ID'''
        response = requests.get(self.base_url + f"categories/{id}", headers=self.headers, verify=False)
        return response.json(), response.status_code

    def post_add_category(self, parameters):
        """ Adds category.
            parameters = {"name":"Category Name",
                          "project_version_id":"<The project version in which the category will be created>",

        OPTIONAL PARAMETERS:
                          "parent_category_id":"<The id of the category where category will be created ( If "
                                               "left null category will be created at the top level )>",
                          "order":"<The position of the category in the category tree ( If left null it will be"
                                  " added to the end of parent)>",
                          "icon":"<Unicode icon, has to be the icon itself e.g. 📜 ( Windows 10 - Winkey + . or "
                                 "Mac ⌃-⌘-Space Bar to open emoji menu )>",
                          "content":"<Category content. Required when category type is page>",
                          "category_type":"<Category type ( 0-Folder, 1-Page, 2-Index)>",
                          "user_id":"Created by user. Required when category type is page"}"""
        response = requests.post(self.base_url + "categories", headers=self.headers, data=json.dumps(parameters),
                                 verify=False)
        return response.json(), response.status_code

    def put_update_category(self, id, parameters):
        ''' Updates category.
        parameters = {"name": "Category Name",
                      "parent_category_id":"<The id of the category where category will be moved "
                                           "(If left null category will be created at the top level)>",
                      "order": "<The position of the category in the category tree ( If left null it will be"
                               " added to the end of parent)>",
                      "icon": "<Unicode icon, has to be the icon itself e.g. 📜 ( Windows 10 - Winkey + . or "
                              "Mac ⌃-⌘-Space Bar to open emoji menu )>",
                      "hidden":"<Hide / Show category>",
                      "language":"<language>"
                      '''
        response = requests.put(self.base_url + f"categories/{id}", headers=self.headers, data=json.dumps(parameters),
                                verify=False)
        return response.json(), response.status_code

    def delete_category(self, id):
        """Deletes a category as per category ID"""
        response = requests.delete(self.base_url + f"categories/{id}", headers=self.headers, verify=False)
        return response.json(), response.status_code


class Article:
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

    def get_article(self, id):
        """returns article as per article ID"""
        response = requests.get(self.base_url + f"articles/{id}/en", headers=self.headers, verify=False)
        return response.json(), response.status_code

    def post_add_article(self, parameters):
        '''Adds an article to an existing category
        parameters needs to be passed in format as below:
        parameters = {
        # MANDATORY_PARAMETERS
            "title": "<Title of the article>",
            "category_id": "<The ID of the category where article will be created>",
            "project_version_id": "<The project version ID in which the article will be created>",
            "user_id": "<The ID of the user that will be marked as an author of this article>",

        # OPTIONAL_PARAMETERS
            "content": "<Markdown content of the article>",
            "order": "<The position of the article in the category tree (Default is end of the category)>"
        }
        '''
        response = requests.post(self.base_url + "articles", headers=self.headers, data=json.dumps(parameters),
                                 verify=False)
        return response.json(), response.status_code

    def put_update_article(self, id, parameters):
        """Updates an article upon sending article ID
           parameters needs to be passed in format as below:
            parameters= {
                 "title": "<Article title>",
                 "content": "<Article markdown content. If editor type is Markdown, use this property>",
                 "html_content": "<Article HTML content. If editor type is WYSIWYG, use this property>",
                 "category_id": "<Move article to another category>",
                 "hidden": "<Hide / Show article>",
                 "version_number": "<Article version to update( Default is latest )>",
                 "translation_option": "<Indicates the translation status of the article. 0 - None , 1 - Need translation, 2 Translated>",
                 "source": "<Free text used for future reference>"
                 }
                 """
        response = requests.put(self.base_url + f"articles/{id}/en", headers=self.headers, data=json.dumps(parameters),
                                verify=False)
        return response.json(), response.status_code

    def delete_article(self, id):
        """Deletes an article with an article ID"""
        response = requests.delete(self.base_url + f"articles/{id}", headers=self.headers, verify=False)
        return response.json(), response.status_code

    def post_publish_article(self, id, parameters):
        """Publishes an article with an article id

        parameters needs to be passed in format as below:
            parameters= {
                         "version_number": "<The version number to be published. Minimum Value 1>",
                         "user_id": "<The id of the user that will be marked as an author of this publish>"
                         }
                         """
        response = requests.post(self.base_url + f"articles/{id}/en/publish", headers=self.headers,
                                 data=json.dumps(parameters), verify=False)
        return response.json(), response.status_code

    def put_fork_article(self, id, parameters):
        """Forks an article with article id

        parameters needs to be passed in format as below:
            parameters= {
            # ALL_MANDATORY
                         "version_number": "<The version number to be published. Minimum Value 1>",
                         "user_id": "<The id of the user that will be marked as an author of this publish>",
                         "lang_code": "<Language code for multilingual>"
                         }
        """
        response = requests.put(self.base_url + f"articles/{id}/fork", headers=self.headers,
                                data=json.dumps(parameters), verify=False)
        return response.json(), response.status_code


class Bulk_Articles:
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

    def post_bulk_add_articles(self, parameters):
        """
        Adds several articles

        parameters needs to be passed in format as below. It should be an array:
               parameters = [
                            {
                        # MANDATORY_PARAMETERS
                            "title": "<Title of the article>",
                            "category_id": "<The ID of the category where article will be created>",
                            "project_version_id": "<The project version ID in which the article will be created>",
                            "user_id": "<The ID of the user that will be marked as an author of this article>",

                        # OPTIONAL_PARAMETERS
                            "content": "<Markdown content of the article>",
                            "order": "<The position of the article in the category tree (Default is end of the category)>",
                            }
                            ]
            """
        response = requests.post(self.base_url + f"/articles/bulkcreate", headers=self.headers,
                                 data=json.dumps(parameters), verify=False)
        return response.json(), response.status_code

    def put_bulk_update_articles(self, parameters):
        """
        Edits list of articles

        parameters needs to be passed in format as below. It should be an array:
        parameters = [
                     {
                # MANDATORY_PARAMETERS
                      "article_id": "<ID of the article>",
                      "lang_code": "<Language code for multilingual>",
                      "version_number": "<Article version to update( Default is latest )>",

                # OPTIONAL_PARAMETERS
                      "title": "<New article title>",
                      "content": "<New article markdown content>",
                      "category_id": "<Move article to another category>",
                      "hidden": "<Hide / Show article>",
                      "translation_option": "<Indicates the translation status of the article. 0 - Not applicable, 1 - Need translation, 2 - translated>",
                      "source": "<Free text used for future reference>"
                      }
                      ]"""

        response = requests.put(self.base_url + "/articles/bulkupdate", headers=self.headers,
                                data=json.dumps(parameters), verify=False)
        return response.json(), response.status_code

    def delete_bulk_articles(self, parameters):
        """Deletes list of articles based on article ids.

           parameters needs to be passed in format as below:
                parameters = {"article_ids": [<list of IDs of articles in sting format>]}
        """

        response = requests.delete(self.base_url + "/articles/bulkdelete", headers=self.headers, params=parameters,
                                   verify=False)
        return response.json(), response.status_code

    def post_bulk_publish_articles(self, parameters):
        """Publishes list of articles in respective language
           parameters needs to be passed in format as below. It should be an array:
                parameters = [
                                {
                                    "article_id": "<ID of the article>",
                                    "version_number": "<The version number to be published. Minimum Value 1>",
                                    "user_id": "<The id of the user that will be marked as an author of this publish>"
                                }
                             ]
                """
        response = requests.post(self.base_url + f"/articles/bulkpublish/en", headers=self.headers,
                                 data=json.dumps(parameters),
                                 verify=False)
        return response.json(), response.status_code


class Misc_Articles:
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

    def get_article_settings(self, id):
        """Get settings for the article based on its ID"""
        response = requests.get(self.base_url + f"/articles/{id}/en/settings", headers=self.headers, verify=False)
        return response.json(), response.status_code

    def get_article_versions(self, id):
        """Get versions for the article based on its ID"""
        response = requests.get(self.base_url + f"/articles/{id}/en/versions", headers=self.headers, verify=False)
        return response.json(), response.status_code

    def get_article_by_version(self, id, version):
        """Get a specific version for the article based on its ID"""
        response = requests.get(self.base_url + f"/articles/{id}/en/versions/{version}", headers=self.headers,
                                verify=False)
        return response.json(), response.status_code

    def put_update_article_setting(self, id, parameters=None):
        """Updates settings for the article in respective language

           parameters needs to be passed in format as below:
            parameters = {"slug": "<The slug of the article>",
                          "seo_title": "<The SEO title of the article>",
                          "description": "<The description of the article>",
                          "allow_comments": "<Disable / Enable internal commenting on the article>",
                          "show_table_of_contents": "<Disable / Enable article table of the contents on the knowledge base>",
                          "tags": "<Custom article tags>",
                          "status_indicator": "<User site article status 0 - none, 1 - new, 2 - updated>",
                          "status_indicator_expiry_date": "<The date time when the public article status is removed>",
                          "exclude_from_search": "<Exclude article from search results on knowledge base>",
                          "related_articles": "<list of related article IDs to show on knowledge base>"
                          }
                          """

        response = requests.put(self.base_url + f"/articles/{id}/en/settings", headers=self.headers,
                                data=json.dumps(parameters), verify=False)
        return response.json(), response.status_code

    def delete_article_version(self, id, version):
        """deletes the version of the article based on article ID and version number"""
        response = requests.delete(self.base_url + f"/articles/{id}/en/version/{version}", headers=self.headers,
                                   verify=False)
        return response.json(), response.status_code


class Reader_Group:
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

    def get_reader_group(self):
        """Gets a summary of all reader groups in the project."""
        response = requests.get(self.base_url + "readers/groups", headers=self.headers, verify=False)
        return response.json(), response.status_code

    def get_one_reader_group(self, groupID):
        """Get summary of one reader groups as per group ID"""
        response = requests.get(self.base_url + f"readers/groups/{groupID}", headers=self.headers, verify=False)
        return response.json(), response.status_code

    def post_add_group(self, parameters):
        """Adds a reader group to the project.

            parameters needs to be passed in format as below:
        parameters = {
            # MANDATORY_PARAMETER
                      "title": "<The name of the reader group.>",

            # OPTIONAL_PARAMETER
                      "description": "<Description of the reader group.>",
                      "associated_readers": "<List of reader IDs to be associated with this reader group.>",
                      "access_scope": "<Access scope of this reader group. Please see format details below>"
                      }

        access_scope =
            {
            "access_level":"The access level for the reader group. 1-Category, 2-Version, 3-Project.",
            "categories":[<List of category IDs. Mandatory when access_level is 1-Category>],
            "project_versions":[<List of project version IDs the reader group has access to.
                                Mandatory when access_level is 2-Version.>]
            }

        """

        response = requests.post(self.base_url + "readers/groups", headers=self.headers, data=json.dumps(parameters),
                                 verify=False)
        return response.json(), response.status_code

    def put_update_group(self, parameters):
        """Updates a reader group.

            parameters needs to be passed in format as below:
            parameters = {
                # MANDATORY_PARAMETER
                    "reader_group_id": "<The ID of the reader group.>",
                    "title": "<The name of the reader group.>",

                # OPTIONAL_PARAMETER
                    "description": "<Description of the reader group.>",
                    "associated_readers": "<List of reader IDs to be associated with this reader group.>",
                    "access_scope": "<Access scope of this reader group.>"
                         }
        """
        response = requests.put(self.base_url + "readers/groups", headers=self.headers, data=json.dumps(parameters),
                                verify=False)
        return response.json(), response.status_code

    def delete_reader_group(self, groupID):
        """Deletes a reader group with the given group ID"""
        response = requests.delete(self.base_url + f"readers/groups/{groupID}", headers=self.headers, verify=False)
        return response.json(), response.status_code


class Reader:
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

    def get_readers(self):
        """gets all readers in project"""
        response = requests.get(self.base_url + "readers", headers=self.headers, verify=False)
        return response.json(), response.status_code

    def post_add_reader(self, parameters):
        """Adds a reader to the project

        parameters needs to be passed in format as below:
         parameters = {
            # MANDATORY_PARAMETERS
                        "email_id": "<The Email address of the reader>",
            # OPTIONAL_PARAMETERS
                        "associated_reader_groups": "<List of reader group IDs.>"
                      }
                      """
        response = requests.post(self.base_url + "readers", headers=self.headers,
                                 data=json.dumps(parameters), verify=False)
        return response.json(), response.status_code

    def put_update_reader(self, parameters):
        """Updates a reader in the project
                parameters needs to be passed in format as below:
                 parameters = {
                    # MANDATORY_PARAMETERS
                                "reader_id": "<The ID of the reader>",
                    # OPTIONAL_PARAMETERS
                                "associated_reader_groups": "<List of reader group IDs.>"
                              }
                              """
        response = requests.put(self.base_url + "readers", headers=self.headers,
                                data=json.dumps(parameters), verify=False)
        return response.json(), response.status_code

    def delete_reader(self, readerID):
        """Deletes a reader in the project"""
        response = requests.delete(self.base_url + f"readers/{readerID}", headers=self.headers,
                                   verify=False)
        return response.json(), response.status_code
