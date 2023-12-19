from flask import jsonify, make_response, request, send_file
from sqlalchemy.exc import SQLAlchemyError

from Server.models.base import db
from Server.models.component import Component
from Server.models.category import Category
from Server.models.brand import Brand
from Server.models.store import Store

from Server.services.barcode import BarcodeService  # Uncomment if barcode service is used


def index():
    return 'Components index'


def components():
    res = []
    try:
        components = db.session.query(Component, Category, Brand, Store).join(Category).join(Brand).join(Store).all()
        if not components:
            return make_response(jsonify("Error querying components"), 404)

        for component_res in components:
            component_dict = component_res[0].as_dict()
            category_dict = component_res[1].as_dict()
            brand_dict = component_res[2].as_dict()
            store_dict = component_res[3].as_dict()

            component_dict.pop('category_id')
            component_dict['category'] = category_dict['name']

            component_dict.pop('brand_id')
            component_dict['brand'] = brand_dict['name']

            component_dict.pop('store_id')
            component_dict['store'] = store_dict['name']

            res.append(component_dict)
        return make_response(jsonify(res), 200)
    except SQLAlchemyError as e:
        return make_response(jsonify('Error querying components: {}'.format(e)), 500)


def add_component():
    component_raw = request.json
    category = db.session.query(Category).filter(Category.name == component_raw['category']).first()
    if category is None:
        category = Category(name=component_raw['category'])
        db.session.add(category)
        db.session.flush()
    brand = db.session.query(Brand).filter(Brand.name == component_raw['brand']).first()
    if brand is None:
        brand = Brand(name=component_raw['brand'])
        db.session.add(brand)
        db.session.flush()
    store = db.session.query(Store).filter(Store.name == component_raw['store']).first()
    if store is None:
        store = Store(name=component_raw['store'])
        db.session.add(store)
        db.session.flush()

    component = Component(name=component_raw['name'],
                          category_id=category.category_id,
                          brand_id=brand.brand_id,
                          store_id=store.store_id,
                          price=component_raw['price'],
                          description=component_raw['description'],
                          stock_quantity=component_raw['stock_quantity'],
                          barcode=component_raw['barcode'])
    component.category = category
    component.brand = brand
    component.store = store

    # generate barcode (if needed)

    try:
        db.session.add(component)
        db.session.commit()
        BarcodeService.generate(component.barcode)  # Uncomment if barcode service is used
        return make_response(jsonify({'message': 'Component added successfully'}), 201)
    except Exception as err:
        print(err)
        return make_response(jsonify({'message': 'Error adding component', 'error': f'{err}'}), 503)


def read_barcode():
    # call service with barcode reader
    barcode_file = request.files['barcode_file']
    barcode_file.save('barcode_file.png')
    barcode = BarcodeService.scan('barcode_file.png')
    if barcode is None:
        print("No barcode")
        return make_response(jsonify({'message': 'No barcode found in image'}), 400)
    else:
        try:
            component = (db.session.query(Component, Category, Brand, Store)
                         .join(Category).join(Brand).join(Store)
                         .filter(Component.barcode == barcode)).first()
            if component is None:
                return make_response(jsonify({'message': 'No component found in database for the given barcode'}), 404)
            else:
                component_dict = component[0].as_dict()
                category_dict = component[1].as_dict()
                brand_dict = component[2].as_dict()
                store_dict = component[3].as_dict()

                component_dict.pop('category_id')
                component_dict['category'] = category_dict['name']

                component_dict.pop('brand_id')
                component_dict['brand'] = brand_dict['name']

                component_dict.pop('store_id')
                component_dict['store'] = store_dict['name']
                print(component_dict)
                return make_response(jsonify(component_dict), 200)
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return make_response(jsonify(error), e.code)
