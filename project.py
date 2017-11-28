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


#JSON APIs to view catalog information

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


#Show all restaurants
@app.route('/')
@app.route('/category/')
def showCategories():
  categories = session.query(CatalogCategory).order_by(asc(CatalogCategory.name))
  return render_template('restaurants.html', restaurants = categories)

#Create a new restaurant
@app.route('/category/new/', methods=['GET','POST'])
def newCategory():
  if request.method == 'POST':
      newCategory = CatalogCategory(name = request.form['name'])
      session.add(newCategory)
      flash('New Category %s Successfully Created' % newCategory.name)
      session.commit()
      return redirect(url_for('showCategory'))
  else:
      return render_template('newRestaurant.html')

#Edit a restaurant
@app.route('/restaurant/<int:restaurant_id>/edit/', methods = ['GET', 'POST'])
def editRestaurant(restaurant_id):
  editedRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
  if request.method == 'POST':
      if request.form['name']:
        editedRestaurant.name = request.form['name']
        flash('Restaurant Successfully Edited %s' % editedRestaurant.name)
        return redirect(url_for('showRestaurants'))
  else:
    return render_template('editRestaurant.html', restaurant = editedRestaurant)


#Delete a restaurant
@app.route('/restaurant/<int:restaurant_id>/delete/', methods = ['GET','POST'])
def deleteRestaurant(restaurant_id):
  restaurantToDelete = session.query(Restaurant).filter_by(id = restaurant_id).one()
  if request.method == 'POST':
    session.delete(restaurantToDelete)
    flash('%s Successfully Deleted' % restaurantToDelete.name)
    session.commit()
    return redirect(url_for('showRestaurants', restaurant_id = restaurant_id))
  else:
    return render_template('deleteRestaurant.html',restaurant = restaurantToDelete)

#Show a restaurant menu #YOU ARE HERE
@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/item/')
def showCategory(category_id):
    category = session.query(CatalogCategory).filter_by(id = category_id).one()
    items = session.query(CatalogItem).filter_by(catalog_category_id = category_id).all()
    return render_template('menu.html', items = items, restaurant = category)
     


#Create a new menu item
@app.route('/restaurant/<int:restaurant_id>/menu/new/',methods=['GET','POST'])
def newMenuItem(restaurant_id):
  restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
  if request.method == 'POST':
      newItem = MenuItem(name = request.form['name'], description = request.form['description'], price = request.form['price'], course = request.form['course'], restaurant_id = restaurant_id)
      session.add(newItem)
      session.commit()
      flash('New Menu %s Item Successfully Created' % (newItem.name))
      return redirect(url_for('showMenu', restaurant_id = restaurant_id))
  else:
      return render_template('newmenuitem.html', restaurant_id = restaurant_id)

#Edit a menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):

    editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['course']:
            editedItem.course = request.form['course']
        session.add(editedItem)
        session.commit() 
        flash('Menu Item Successfully Edited')
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = editedItem)


#Delete a menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods = ['GET','POST'])
def deleteMenuItem(restaurant_id,menu_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    itemToDelete = session.query(MenuItem).filter_by(id = menu_id).one() 
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Menu Item Successfully Deleted')
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('deleteMenuItem.html', item = itemToDelete)




if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 5000)
