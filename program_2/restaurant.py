import math
from json import JSONEncoder, dumps

class Restaurant():
  def __init__(self, obj):
    self.id = obj['id']
    self.restaurant_name = obj['restaurant_name']
    self.rating = obj['rating']
    self.distance_from_me = obj['distance_from_me']
    self.score = self.calculate_score()

  # Function for comparison
  def __lt__(self, other):
    # First compare the score (desc)
    # If same score, compare the rating (desc)
    # If same rating, compare the distance (desc)
    # If same distance, compare the name (asc)
    if self.score != other.score:
      return self.score < other.score
    elif self.rating != other.rating:
      return self.rating < other.rating
    elif self.distance_from_me != other.distance_from_me:
      return self.distance_from_me < other.distance_from_me
    elif self.restaurant_name != other.restaurant_name:
      return self.restaurant_name.lower() > other.restaurant_name.lower()
    else:
      return False


  def __repr__(self):
    return dumps(self, cls=RestaurantEncoder)

  # Function to calculate the score
  def calculate_score(self):
    score = (self.rating * 10 - self.distance_from_me * 0.5 + math.sin(self.id) * 2.00)* 100 + 0.5
    return round((score / 100), 2)


class RestaurantEncoder(JSONEncoder):
  def default(self, o):
    return { 
      'id': o.id,
      'restaurant_name': o.restaurant_name,
      'rating': o.rating,
      'distance_from_me': o.distance_from_me,
      'score': o.score
    }