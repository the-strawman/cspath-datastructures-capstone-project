from trie import Trie
from data import *
from welcome import *
from hashmap import HashMap
from linkedlist import LinkedList

# Printing the Welcome Message
print_welcome()

# Entering cuisine data
food_types = Trie()
eateries = HashMap(len(types))
for food in types:
    food_types.add(food)
    eateries.assign(food, LinkedList())

# restaurant data-point key names:
eatery_cuisine = "cuisine"
eatery_name = "name" 
eatery_price = "price"
eatery_rating = "rating"
eatery_address = "address"
# Entering restaurant data
for restaurant in restaurant_data:
    current_eateries_for_cuisine = eateries.retrieve(restaurant[0])
    current_eatery_data = HashMap(len(restaurant))
    current_eatery_data.assign(eatery_cuisine, restaurant[0])
    current_eatery_data.assign(eatery_name, restaurant[1])
    current_eatery_data.assign(eatery_price, restaurant[2])
    current_eatery_data.assign(eatery_rating, restaurant[3])
    current_eatery_data.assign(eatery_address, restaurant[4])
    if current_eateries_for_cuisine.get_head_node().get_value() is None:
        current_eateries_for_cuisine.get_head_node().value = current_eatery_data
    else:
        current_eateries_for_cuisine.insert_beginning(current_eatery_data)

# Begin user interaction logic
quit_code = "quit!"
def quit_sequence():
  print("\nThanks for using SoHo Restaurants!")
  exit()

intro_text = """
What type of food would you like to eat?
Type that food type (or the beginning of that food type) and press enter to see if it's here.
(Type \"{0}\" at any point to exit.)
""".format(quit_code)
partial_match_text = """
Type a number to select a corresponding cuisine.
Or type the beginning of your preferred cuisine to narrow down the options.
"""

while True:
  # What cuisine are we looking for?
  user_input = str(input(intro_text)).lower()

  if user_input == quit_code:
    quit_sequence()
  # First try a full-text match
  my_cuisine = food_types.get(user_input)
  if not my_cuisine:
    print("Couldn't find \"{0}\".".format(user_input.title()))
  
  # if no match on full-text search, try prefix search
  while not my_cuisine:
    available_cuisines = food_types.find(user_input)
    if not available_cuisines:
      # a prefix search found nothing, so return the whole list of available cuisines
      available_cuisines = food_types.find("")
      print("Here is the list of available cuisines:\n")
    else:
      print("Here are some matches from the available cuisines:\n")
    
    idx = 0
    for cuisine in available_cuisines:
      idx += 1
      print("{0} - {1}".format(idx, cuisine.title()))
    available_cuisines_response = input(partial_match_text)
    if available_cuisines_response == quit_code:
      quit_sequence()
    # the user input could be an int or a str.
    # try to process an int value, a ValueError exception indicates non-int input
    try:
      idx = int(available_cuisines_response) - 1
      print("Search for {0} restaurants?".format(available_cuisines[idx].title()))
      user_response = str(input("(Hit [enter]/[return] for 'yes'; type 'no' to perform a new search.) ")).lower()
      if user_response == quit_code:
        quit_sequence()
      elif user_response in ["", "y", "yes", "[enter]", "[return]", "enter", "return"]:
        my_cuisine = available_cuisines[idx]
      else:
        user_input = None
    except ValueError:
      available_cuisines_response = str(available_cuisines_response).lower()
      my_cuisine = food_types.get(available_cuisines_response)
      if not my_cuisine:
        user_input = available_cuisines_response
  
  # Now we have a cuisine, let's retrieve the restaurants & present the data
  my_eateries = eateries.retrieve(my_cuisine)
  current_node = my_eateries.get_head_node()
  print("\n{} restauants in SoHo".format(my_cuisine.title()))
  print("-"*20)
  while current_node:
    eatery = current_node.get_value()
    print('{:<14}{}'.format("Restaurant:", eatery.retrieve(eatery_name)))
    print("{:<14}{}".format("Price:", "$" * int(eatery.retrieve(eatery_price))))
    print("{:<14}{}".format("Rating:", "*" * int(eatery.retrieve(eatery_rating))))
    print("{:<14}{}".format("Address:", eatery.retrieve(eatery_address)))
    print("-"*20)
    current_node = current_node.get_next_node()
    
  user_response = str(input("\nWould you like to look for restaurants matching a different cuisine? ")).lower()
  if user_response in ["n", "no", "q", "quit", "x", "exit", quit_code]:
    quit_sequence()
