from flask import Flask, render_template, request, redirect,jsonify, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, CatalogCategory, CatalogItem

#Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()



#JSON APIs to view catalog information [DONE]
@app.route('/category/<int:category_id>/item/JSON')
def categoryItemJSON(category_id):
    category = session.query(CatalogCategory).filter_by(id = category_id).one()
    items = session.query(CatalogItem).filter_by(catalog_category_id = category_id).all()
    return jsonify(Items=[i.serialize for i in items])

@app.route('/category/<int:category_id>/item/<int:item_id>/JSON')
def itemDetailJSON(category_id, item_id):
    item = session.query(CatalogItem).filter_by(id = item_id).one()
    return jsonify(Item = item.serialize)

@app.route('/category/JSON')
def categoriesJSON():
    categories = session.query(CatalogCategory).all()
    return jsonify(Cateogries= [c.serialize for c in categories])



#Show all restaurants [rename]
@app.route('/')
@app.route('/category/')
def showCategories():
  categories = session.query(CatalogCategory).order_by(asc(CatalogCategory.name))
  return render_template('restaurants.html', restaurants = categories)

#Create a new restaurant [done - rename]
@app.route('/category/new/', methods=['GET','POST'])
def newCategory():
  if request.method == 'POST':
      newCategory = CatalogCategory(name = request.form['name'])
      session.add(newCategory)
      flash('New Category %s Successfully Created' % newCategory.name)
      session.commit()
      return redirect(url_for('showCategories'))
  else:
      return render_template('newRestaurant.html')

#Edit a category [done - rename]
@app.route('/restaurant/<int:category_id>/edit/', methods = ['GET', 'POST'])
def editCategory(category_id):
  editedCategory = session.query(CatalogCategory).filter_by(id = category_id).one()
  if request.method == 'POST':
      if request.form['name']:
        editedCategory.name = request.form['name']
        flash('Category Successfully Edited %s' % editedCategory.name)
        return redirect(url_for('showCategories'))
  else:
    return render_template('editRestaurant.html', category = editedCategory)

#Delete a restaurant [done - rename]
@app.route('/restaurant/<int:category_id>/delete/', methods = ['GET','POST'])
def deleteCategory(category_id):
  categoryToDelete = session.query(CatalogCategory).filter_by(id = category_id).one()
  if request.method == 'POST':
    session.delete(categoryToDelete)
    flash('%s Successfully Deleted' % categoryToDelete.name)
    session.commit()
    return redirect(url_for('showCategories', restaurant_id = category_id))
  else:
    return render_template('deleteRestaurant.html',restaurant = categoryToDelete)

#Show a category's items [done - rename]
@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/item/')
def showCategory(category_id):
    category = session.query(CatalogCategory).filter_by(id = category_id).one()
    items = session.query(CatalogItem).filter_by(catalog_category_id = category_id).all()
    return render_template('menu.html', items = items, restaurant = category)
     
#Create a new menu item [done - rename]
@app.route('/restaurant/<int:category_id>/menu/new/',methods=['GET','POST'])
def newCatalogItem(category_id):
  category = session.query(CatalogCategory).filter_by(id = category_id).one()
  if request.method == 'POST':
      newCatalogItem = CatalogItem(name = request.form['name'], description = request.form['description'], catalog_category_id = category_id)
      session.add(newCatalogItem)
      session.commit()
      flash('New Menu %s Item Successfully Created' % (newCatalogItem.name))
      return redirect(url_for('showCategory', category_id = category_id))
  else:
      return render_template('newmenuitem.html', restaurant_id = category_id)

#Edit a menu item
@app.route('/restaurant/<int:category_id>/menu/<int:item_id>/edit', methods=['GET','POST'])
def editCatalogItem(category_id, item_id):
    editedCatalogItem = session.query(CatalogItem).filter_by(id = item_id).one()
    category = session.query(CatalogCategory).filter_by(id = category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedCatalogItem.name = request.form['name']
        if request.form['description']:
            editedCatalogItem.description = request.form['description']
        session.add(editedCatalogItem)
        session.commit() 
        flash('Catalog Item Successfully Edited')
        return redirect(url_for('showCategory', category_id = category_id))
    else:
        return render_template('editmenuitem.html', category_id = category_id, item_id = item_id, item = editedCatalogItem)

#Delete a menu item
@app.route('/restaurant/<int:category_id>/menu/<int:item_id>/delete', methods = ['GET','POST'])
def deleteCatalogItem(category_id,item_id):
    category = session.query(CatalogCategory).filter_by(id = category_id).one()
    catalogItemToDelete = session.query(CatalogItem).filter_by(id = item_id).one() 
    if request.method == 'POST':
        session.delete(catalogItemToDelete)
        session.commit()
        flash('Menu Item Successfully Deleted')
        return redirect(url_for('showCategory', category_id = category_id))
    else:
        return render_template('deleteMenuItem.html', item = catalogItemToDelete)



if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 5000)
