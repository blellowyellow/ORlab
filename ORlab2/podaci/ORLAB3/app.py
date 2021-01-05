from flask import Flask, request, jsonify, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import json
import os

#app init
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

#DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqllite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#DB init
db = SQLAlchemy(app)
#MA init
ma = Marshmallow(app)

#Vrt Model
class Vrt(db.Model):
    sifra = db.Column(db.Integer, primary_key=True, nullable=False)
    naziv = db.Column(db.String(100), nullable=False)
    wiki = db.Column(db.String(100), nullable=False)
    latnaziv = db.Column(db.String(100), nullable=False)
    # bojaploda = db.Column(db.String(100), nullable=False)
    # izgledsjemena = db.Column(db.String(100), nullable=False)
    # jestiva = db.Column(db.String(100), nullable=False)
    # sadnja = db.Column(db.String(100), nullable=False)
    # berba = db.Column(db.String(100), nullable=False)
    # tipsadnje = db.Column(db.String(100), nullable=False)
    # nazivmjesta = db.Column(db.String(100), nullable=False)
    # vrstamjesta = db.Column(db.String(100), nullable=False)

    def __init__(self, naziv, wiki, latnaziv):
        # bojaploda, izgledsjemena, jestiva, sadnja, berba, tipsadnje, nazivmjesta, vrstamjesta):
        self.naziv = naziv
        self.wiki = wiki
        self.latnaziv = latnaziv
        # self.bojaploda = bojaploda
        # self.izgledsjemena = izgledsjemena
        # self.jestiva = jestiva
        # self.sadnja = sadnja
        # self.berba = berba
        # self.tipsadnje = tipsadnje
        # self.nazivmjesta = nazivmjesta
        # self.vrstamjesta = vrstamjesta


class VrtSchema(ma.Schema):
    class Meta:
     fields= ("sifra", "naziv", "wiki", "latnaziv")

many_schema = VrtSchema(many=True)

@app.route('/product', methods=['POST'])
def add_entry():
    try:
        naziv = request.json['naziv']
        wiki = request.json['wiki']
        latnaziv = request.json['latnaziv']
        # bojaploda = request.json['bojaploda']
        # izgledsjemena = request.json['izgledsjemena']
        # jestiva = request.json['jestivo']
        # sadnja = request.json['sadnja']
        # berba = request.json['berba']
        # tipsadnje = request.json['tipsadnje']
        # nazivmjesta = request.json['nazivmjesta']
        # vrstamjesta = request.json['vrstamjesta']
    except Exception as e:
        return make_response(jsonify({'status': "Can not create",
                        'message': "Please provide all parameters",
                        'response': None}), 400)
    new_entry = Vrt(naziv, wiki, latnaziv)
    db.session.add(new_entry)
    db.session.commit()

    sifra=new_entry.sifra

    return make_response(jsonify({'status': "OK",
                        'message': "Added Vrt entry",
                        'response': {'sifra' : sifra,
                                     'naziv': naziv,
                                     'wiki': wiki,
                                     'latnaziv': latnaziv,
                                     },
                        'links': {'self': url_for('get_single_entry', sifra=sifra),
                                  'all': url_for('get_all_entries')
                                  }
                        }), 200)



@app.route('/product', methods=['GET'])
def get_all_entries():
    all_entries = Vrt.query.all()
    result = many_schema.dump(all_entries)
    return jsonify(result)

@app.route('/product/<int:sifra>', methods=['GET'])
def get_single_entry(sifra):
    entry = Vrt.query.get(sifra)
    if entry is not None:
        return make_response(jsonify({'status' : "OK",
                        'message': "Fetched Vrt entry",
                        'response': {'sifra' : entry.sifra,
                                     'naziv' : entry.naziv,
                                     'wiki' : entry.wiki,
                                     'latnaziv' : entry.latnaziv,

                              },
                         'links': {'self' : url_for('get_single_entry', sifra=sifra),
                                   'all' : url_for('get_all_entries')
                             }
                     }), 200)
    else:
        return make_response(jsonify({'status': "Not found",
                        'message': "Plant with provided ID does not exist",
                        'response': None}), 400)

@app.route('/product/<sifra>', methods=['PUT'])
def update_entry(sifra):
    entry = Vrt.query.get(sifra)
    if entry is None:
        return make_response(jsonify({'status': "Can not update",
                        'message': "Entry with provided ID does not exist",
                        'response': None}), 400)
    # stupci= [entry.naziv, entry.wiki, entry.latnaziv, entry.bojaploda, entry.izgledsjemena, entry.jestiva, entry.sadnja, entry.berba, entry.tipsadnje, entry.nazivmjesta, entry.vrstamjesta]
    # vrijednosti = [request.json['naziv'],
    #     request.json['wiki'],
    #     request.json['latnaziv'],
    #     request.json['bojaploda'],
    #     request.json['izgledsjemena'],
    #     request.json['jestivo'],
    #     request.json['sadnja'],
    #     request.json['berba'],
    #     request.json['tipsadnje'],
    #     request.json['nazivmjesta'],
    #     request.json['vrstamjesta']]
    # for (stupac, vrijednost) in zip(stupci, vrijednosti):
    #     if vrijednost is not None:
    #         stupac=vrijednost
    #     else:
    #         stupac=stupac


    try:
        naziv = request.json['naziv']
        wiki = request.json['wiki']
        latnaziv = request.json['latnaziv']
        # bojaploda = request.json['bojaploda']
        # izgledsjemena = request.json['izgledsjemena']
        # jestiva = request.json['jestivo']
        # sadnja = request.json['sadnja']
        # berba = request.json['berba']
        # tipsadnje = request.json['tipsadnje']
        # nazivmjesta = request.json['nazivmjesta']
        # vrstamjesta = request.json['vrstamjesta']
    except Exception as e:
        return make_response(jsonify({'status': "Can not update",
                 'message': "Please provide all entries",
                 'response': None}), 400)

    entry.naziv = naziv
    entry.wiki = wiki
    entry.latnaziv = latnaziv
    # entry.bojaploda = bojaploda
    # entry.izgledsjemena = izgledsjemena
    # entry.jestiva = jestiva
    # entry.sadnja = sadnja
    # entry.berba = berba
    # entry.tipsadnje = tipsadnje
    # entry.nazivmjesta = nazivmjesta
    # entry.vrstamjesta = vrstamjesta

    db.session.commit()
    entry = Vrt.query.get(sifra)
    return make_response(jsonify({'status': "OK",
             'message': "Updated Vrt entry",
             'response': {'sifra' : entry.sifra,
                          'naziv': entry.naziv,
                          'wiki': entry.wiki,
                          'latnaziv': entry.latnaziv,
                          },
             'links': {'self': url_for('get_single_entry', sifra=sifra),
                       'all': url_for('get_all_entries')
                       }
             }), 200)
    #return one_schema.dump(entry)

@app.route('/product/<sifra>', methods=['DELETE'])
def delete_entry(sifra):
    entry = Vrt.query.get(sifra)
    if entry is None:
        return make_response(jsonify({'status': "Not found",
                        'message': "Entry with provided ID does not exist",
                        'response': None}), 400)
    db.session.delete(entry)
    db.session.commit()
    if entry is not None:
        return make_response(jsonify({'status' : "OK",
                        'message': "Entry was deleted"}), 200)

@app.route('/product/openapi', methods=['GET'])
def get_open_api():
    f=open("openapi.json")
    data = json.load(f)
    return jsonify(data)

@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify({"404" : "Resource not found"}), 404)

if __name__ == '__main__':
    app.run(debug=True)
