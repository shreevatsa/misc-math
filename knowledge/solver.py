import parser

def solve(possibilities, projections, dialogue, goal):
  dialogue = dialogue.replace(goal, '<goal>')
  statements = parser.parse(dialogue)
  for (speaker, parts) in statements:
    # print '%s: %s' % (speaker, parts)
    assert speaker in projections.keys()
  return real_solve(possibilities, projections, statements)

def real_solve(possibilities, projections, statements):
  def project(space, player):
    shards = {}
    for possibility in space:
      projection = projections[player](possibility)
      if projection not in shards: shards[projection] = set()
      shards[projection].add(possibility)
    return shards
  
  space = {}
  space[0] = possibilities[:]
  for i in range(len(statements)):
    (speaker, statement_parts) = statements[i]
    space[i + 1] = space[i]
    for part in statement_parts:
      assert 0 <= part.time <= i
      shards = project(space[part.time], part.whose_information)
      func = lambda key : (len(shards[key]) == 1 if part.knowledge else len(shards[key]) > 1)
      if part.whose_information == speaker:
        ok_keys = [key for key in shards if func(key)]
      else:
        ok_keys_other = set(key for key in shards if func(key))
        shards = project(space[i], speaker)
        ok_keys = []
        for key in shards:
          if all(projections[part.whose_information](value) in ok_keys_other for value in shards[key]):
            ok_keys.append(key)
      new_space = []
      for key in ok_keys:
        new_space.extend(shards[key])
      space[i + 1] = [value for value in space[i + 1] if value in new_space]
    # print 'After statement', i, 'space of possibilities:', space[i + 1]
  return space[i + 1]


