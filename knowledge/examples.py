import solver


def example1():
  '''Sum-product puzzle'''
  possibilities = [(x, y) for x in range(2, 101) for y in range(x + 1, 101) if x + y <= 100]
  projections = {  # SUMit knows the SUM; PRiya knows the PRoduct.
    'Sumit':  lambda (x, y): x + y,
    'Priya': lambda (x, y): x * y
  }
  dialogue = '''
    Sumit: Priya does not know X and Y.
    Priya: Now I know X and Y.
    Sumit: Now I also know X and Y!
  '''
  return solver.solve(possibilities, projections, dialogue, 'X and Y')


class Cheryl:
  '''Cheryl's birthday'''
  possibilities = ['May 15', 'May 16', 'May 19', 'June 17', 'June 18',
                   'July 14', 'July 16', 'August 14', 'August 15', 'August 17']
  projections = {  # Albert gets the month, Bernard gets the date.
    'Albert':  lambda month_date: month_date.split()[0],
    'Bernard': lambda month_date: month_date.split()[1]
  }
  dialogue = '''
    Albert: I don't know when Cheryl's birthday is, but I know that Bernard does not know too.
    Bernard: At first I don't know when Cheryl's birthday is, but I know now.
    Albert: Then I also know when Cheryl's birthday is.
  '''
  goal = "when Cheryl's birthday is"


def example2():
  '''The original Cheryl's birthday problem.'''
  return solver.solve(Cheryl.possibilities, Cheryl.projections, Cheryl.dialogue, Cheryl.goal)


def example3():
  '''Modified problem where August 17 (popular error in original) is correct.'''
  dialogue = "Bernard: I don't know when Cheryl's birthday is." + Cheryl.dialogue
  return solver.solve(Cheryl.possibilities, Cheryl.projections, dialogue, Cheryl.goal)


def example4():
  '''Modified problem without the final statement by Albert.'''
  dialogue = '''
    Albert: I don't know when Cheryl's birthday is, but I know that Bernard does not know too.
    Bernard: At first I don't know when Cheryl's birthday is, but I know now.
  '''
  return solver.solve(Cheryl.possibilities, Cheryl.projections, dialogue, Cheryl.goal)

def example5():
  '''Friedman's puzzle.'''
  possibilities = [(x, y) for x in range(1, 10) for y in range(x, 10)]
  projections = {  # Sam gets sum, Peter gets product.
    'Sam': lambda (x, y): x + y,
    'Peter': lambda (x, y): x * y
  }
  dialogue = '''
    Peter: I don't know the numbers.
    Sam: I don't know the numbers.
    Peter: I don't know the numbers.
    Sam: I don't know the numbers.
    Peter: I don't know the numbers.
    Sam: I don't know the numbers.
    Peter: I don't know the numbers.
    Sam: I don't know the numbers.
    Peter: I know the numbers!
  '''
  return solver.solve(possibilities, projections, dialogue, 'the numbers')


if __name__ == '__main__':
  assert example1() == [(4, 13)]
  assert example2() == ['July 16']
  assert example3() == ['August 17']
  assert example4() == ['July 16', 'August 15', 'August 17']
  assert example5() == [(2, 8)]
