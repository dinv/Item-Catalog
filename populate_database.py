from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import CatalogCategory, CatalogItem, Base, User
 
engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()



category1 = CatalogCategory(name = "Board Games", user_id = 1)
session.add(category1)
session.commit()

item1 = CatalogItem(name = "Settlers of Catan", \
					description = "Picture yourself in the era of discoveries: \
					after a long voyage of great deprivation, your ships have \
					finally reached the coast of an uncharted island. Its name \
					shall be Catan! But you are not the only discoverer. Other \
					fearless seafarers have also landed on the shores of Catan: \
					the race to settle the island has begun!", \
					catalog_category = category1)
session.add(item1)
session.commit()

item2 = CatalogItem(name = "Carcassonne", \
					description = "In Carcassonne, players build the area \
					surrounding this impressive city, one tile at a time. \
					They then place a follower on fields, cities, roads \
					or monasteries in order to score as many points as \
					possible. These followers will become knights, \
					monks, farmers and thieves, depending on where \
					they are placed. No matter their function, the \
					player who will most cleverly use their followers \
					will win the game. Entirely redesigned and modernized, \
					this edition includes two expansions: the river and the abbot.", \
					catalog_category = category1)
session.add(item2)
session.commit()

item3 = CatalogItem(name = "Seven Wonders", \
					description = "You are the leader of one \
					of the 7 great cities of the Ancient World. Gather resources, \
					develop commercial routes and affirm your military supremacy. \
					Build your city and erect an architectural wonder which will \
					transcend future times.", \
					catalog_category = category1)
session.add(item3)
session.commit()


category2 = CatalogCategory(name = "Nintendo Switch", user_id = 1)
session.add(category2)
session.commit()

item1 = CatalogItem(name = "The Legend of Zelda: Breath of the Wild", \
					description = "Step into a world of discovery, exploration, \
					and adventure in The Legend of Zelda: Breath of the Wild, \
					a boundary-breaking new game in the acclaimed series. \
					Travel across vast fields, through forests, and to mountain \
					peaks as you discover what has become of the kingdom of \
					Hyrule in this stunning Open-Air Adventure. Now on the \
					Nintendo Switch console, your journey is freer and more \
					open than ever. Take your system anywhere, and adventure \
					as Link any way you like.", \
					catalog_category = category2)
session.add(item1)
session.commit()

item2 = CatalogItem(name = "Mario Kart 8 Deluxe", \
					description = "Hit the road with the definitive version \
					of Mario Kart 8 and play anytime, any-where! Race your \
					friends or battle them in a revised battle mode on \
					new and returning battle courses. Play locally in up \
					to 4-player multiplayer in 1080p while playing in TV Mode. \
					Every track from the Wii U version, including DLC, \
					makes a glorious return. Plus, the Inklings appear \
					as all-new guest characters, along with returning favorites, \
					such as King Boo, Dry Bones, and Bowser Jr.!", \
					catalog_category = category2)
session.add(item2)
session.commit()

item3 = CatalogItem(name = "Snipperclips", \
					description = "Cut paper characters into new shapes \
					to solve dynamic puzzles and play activities in a \
					wonderfully creative and imaginative world! \
					Work together with friends to cut paper characters \
					into new shapes and solve puzzles - Communicate and \
					cooperate (or not) and move the paper characters on the \
					screen. Get creative and cut shapes out of each other \
					to interact with the environment, move objects, \
					and solve puzzles Dynamic puzzles full of \
					ever-changing gameplay - Use your imagination to \
					solve puzzles of many different types in fun and \
					interesting ways Three different types of modes - \
					Solve basic and advanced puzzles by yourself or with a \
					friend in the main game. Then, work together as a team \
					and solve up to 2-4 player dynamic puzzles or compete \
					against each other in activities!", \
					catalog_category = category2)
session.add(item3)
session.commit()


print "added catalog items!"

