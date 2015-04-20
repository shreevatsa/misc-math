import solver

def example1():
  '''Cheryl's birthday'''
  possibilities = ['May 15', 'May 16', 'May 19', 'June 17', 'June 18',
                   'July 14', 'July 16', 'August 14', 'August 15', 'August 17']
  players = ['Albert', 'Bernard']
  projections = {
    'Albert':  lambda month_date: month_date.split()[0],
    'Bernard': lambda month_date: month_date.split()[1]
  }
  dialogue = '''
    Albert: I don't know when Cheryl's birthday is, but I know that Bernard does not know too.
    Bernard: At first I don't know when Cheryl's birthday is, but I know now.
    Albert: Then I also know when Cheryl's birthday is.
  '''
  goal = "when Cheryl's birthday is"
  return solver.solve(possibilities, players, projections, dialogue, goal)

def example2():
  '''Sum-product puzzle'''
  possibilities = [(x, y) for x in range(2, 101) for y in range(2, 101) if x + y <= 100 and x < y]
  players = ['Sumit', 'Priya']  # SUMit knows the SUM; PRiya knows the PRoduct.
  projections = {
    'Sumit':  lambda (x, y): x + y,
    'Priya': lambda (x, y): x * y
  }
  dialogue = '''
    Sumit: Priya does not know X and Y.
    Priya: Now I know X and Y.
    Sumit: Now I also know X and Y!
  '''
  goal = 'X and Y'
  return solver.solve(possibilities, players, projections, dialogue, goal)

if __name__ == '__main__':
  assert example1() == ['July 16']
  assert example2() == [(4, 13)]
