import ssl
from elasticsearch import Elasticsearch
from elasticsearch.connection import create_ssl_context
from flask import Flask, request, send_from_directory, make_response
import json
import uuid
from shutil import copyfile
import urllib3
import certifi
from flask import Response
from flask import json
from flask import Flask, redirect, url_for, render_template, send_from_directory
import pprint


#disregard tolerable warnings from certification
urllib3.disable_warnings()

#locate template folder for web page template
app = Flask(__name__, template_folder='template')

#connection to ElasticSearch
context = create_ssl_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
es = Elasticsearch(
    ['tux-es1.cci.drexel.edu'],
    http_auth=('erp75', 'seeng7oht9Ke'),
    scheme="https",
    port=9200,
    ssl_context=context,
)

    
#Homepage (base.html as parent template)
@app.route('/', methods = ['POST', 'GET'])
def index(): 
    global content
   
    if request.method == "GET": 
        return render_template('base.html')
    elif 'quickSearch' in request.form:
        keywords = request.form['keyword']
        query_body = {
            "query": {
            "multi_match": {
            "query": keywords,
            "fields": [
                "Title^3", "Description"
            ],
            "fuzziness": "AUTO"
            }
            }
        }
        res = es.search(index="erp75_info624_201904_project_anime5", body=query_body)
        
        content = res['hits']['hits']
        return redirect(url_for("search", srch = keywords))
    elif 'genreSearch' in request.form:
        genre = request.form.getlist("AnimeGenre")
        animeType = request.form['AnimeType']
        animeSort = request.form['AnimeSort']
        animeDate = request.form['AnimeStartDate']
        animeRate = request.form['AnimeRating']
        
        # if animeDate == None:
        #    animeDate = "0000-00-00"
        #    print("hello")

        # print(animeDate + "Hello ")
        genreList = ','
        genreList = genreList.join(genre)
        joinkeywords = ' '
        joinkeywords = genreList +' ' + animeType
        query_body = {
                "from": 0,
                "size": 1500,
                "query": {
                    "bool": {
                    "must": [
                        {
                        "multi_match": {
                            "query": joinkeywords,
                            "type":       "cross_fields",
                            "fields": [
                            "Genres",
                            "Type"
                            ],
                            "operator":   "and"
                        }
                        }
                    ],
                    "filter": [
                        {
                        "range": {
                            "Score": {
                            "gte": animeRate
                            }
                        }
                        }
                    ]
                    
                    }
                }
        }
       
        sort = {'sort':[
                {
                animeSort: {
                    "order": "desc"
                }
                }
            ]}
        dateFilter = {
                    "range": {
                        "Start_airing": {
                        "gte": animeDate
                        }
                    }
                    }
                
        print(request.form['AnimeStartDate'] + "Hello")
        if animeSort != "Relevance":
            query_body.update(sort)
        if animeDate != "":
            query_body["query"]["bool"]["filter"].append(dateFilter)
        print(query_body)
        res = es.search(index="erp75_info624_201904_project_anime5", body=query_body)
        content = res['hits']['hits']
        return redirect(url_for("search", srch = genreList))


#Result for search by name (extend base.html by resultName.html as its child template)
@app.route("/<srch>")
def search(srch):
    return render_template('resultName.html', kw = content)


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
    