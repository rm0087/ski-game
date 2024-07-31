import sqlite3

CONN = sqlite3.connect('ski_game.db')
CURSOR = CONN.cursor()


class Scores:

  all = {}


  def __init__(self, name, score):
    self.id = None
    self.name = name 
    self.score = score


  def __repr__(self):
    return f"<Scores {self.name} {self.score}>"
  
  @classmethod
  def create_table(cls):
    sql = """
      CREATE TABLE IF NOT EXISTS scores (
      id INTEGER PRIMARY KEY, 
      name TEXT, 
      score TEXT )
    """
    CURSOR.execute(sql)
    CONN.commit()

  def save(self):
    sql = """
      INSERT INTO scores (name, score)
      VALUES (?, ?)
    """

    CONN.execute(sql, (self.name, self.score))
    CONN.commit()

    self.id = CURSOR.lastrowid
    type(self).all[self.id] = self


  @classmethod
  def get_top_scores(cls, limit=10):
    sql = """
      SELECT name, score FROM scores
      ORDER BY score DESC
      LIMIT ?
    """
    CURSOR.execute(sql, (limit,))
    return CURSOR.fetchall()
  

Scores.create_table()