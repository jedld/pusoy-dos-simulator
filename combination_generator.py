
def combination_pick(arr, choices, n, depth):
  if (depth >= n):
    arr.sort()
    return [arr]
  combinations = []
  for k in choices:
    arr_copy = choices.copy()
    arr_copy.remove(k)

    arr_stuff = arr.copy()
    arr_stuff.append(k)
    result = combination_pick(arr_stuff, arr_copy, n, depth + 1)
    for r in result:
      if not r in combinations:
        combinations.append(r)
  return combinations


def card_id_to_name(card):
  card_details = []
  
  suite = card // 13
  card_type = card % 13
  
  if suite <= 1:
    card_details.append('black')
  else:
    card_details.append('red')

  if suite == 0:
    card_details.append('club')
  elif suite == 1:
    card_details.append('spade')
  elif suite == 2:
    card_details.append('heart')
  elif suite == 3:
    card_details.append('diamond')
  

  if card_type == 0:
    card_details.append('3')
  elif card_type == 1:
    card_details.append('4')
  elif card_type == 2:
    card_details.append('5')
  elif card_type == 3:
    card_details.append('6')
  elif card_type == 4:
    card_details.append('7')
  elif card_type == 5:
    card_details.append('8')
  elif card_type == 6:
    card_details.append('9')
  elif card_type == 7:
    card_details.append('10')
  elif card_type == 8:
    card_details.append('J')
  elif card_type == 9:
    card_details.append('Q')
  elif card_type == 10:
    card_details.append('K')
  elif card_type == 11:
    card_details.append('A')
  elif card_type == 12:
    card_details.append('2')
  card_details.append(card)
  return card_details

def combination_from_pile(pile):
  card_combination = []
  pile.sort()
  cards_in_hand = [ card_id_to_name(c) for c in pile]

  # straight flushes
  ptr = 0
  straight_flush_list = []
  royal_flush_list = []

  for index in pile:
    candidate = []
    suite_id = index // 13
    for k in range(5):
      card_id = ((index + k) % 13) + 13 * suite_id
      if card_id in pile:
        candidate.append(card_id)
        
    if len(candidate) == 5:
      if candidate[0] % 13 == 8:
        royal_flush_list.append(candidate.copy())
      else:
        straight_flush_list.append(candidate.copy())

  for f in royal_flush_list:
    card_combination.append([0,f])
  for f in straight_flush_list:
    card_combination.append([1,f])

  def sort_by_type(c):
    return c[2]
  def sort_by_index(c):
    return c[3]
  def sort_by_suite(c):
    return c[1]

  cards_in_hand.sort(key=sort_by_type)

  quadro = []
  trio = []
  pair_list = []
  quadro_list = []
  quadro_start = None
  ptr = 0

  while ptr < len(cards_in_hand) - 1:
    _ , suite, card, index = cards_in_hand[ptr]
    if quadro_start == None:
      quadro_start = card
      quadro.append(index)
      ptr += 1
      continue
    if quadro_start==card:
      quadro.append(index)
      if len(quadro) == 2:
        pair_list.append(quadro.copy())
      if len(quadro) == 3:
        trio.append(quadro.copy())
      elif len(quadro) == 4:
        quadro_list.append(quadro.copy())
        quadro_start = None
        quadro = []
      ptr += 1
      continue
    else:
      quadro_start = None
      quadro = []

  # generate quadro + kicker combinations
  for q in quadro_list:
    for c in pile:
      if c not in q:
        q_kicker = q.copy()
        q_kicker.append(c)
        card_combination.append([2, q_kicker])

  # full houses
  for t in trio:
    for p in pair_list:
      if p[0] not in t and p[1] not in t:
        trio_appended = t.copy()
        trio_appended.append(p[0])
        trio_appended.append(p[1])
        card_combination.append([3, trio_appended])
  
  # flush
  suite_dict = {}
  for card in pile:
    suite = card // 13
    cards = suite_dict.get(suite, [])
    cards.append(card)
    suite_dict[suite] = cards

  for suite in suite_dict.keys():
    same_suite_combinations = combination_pick([], suite_dict[suite], 5, 0)
    for c in same_suite_combinations:
      card_combination.append([4, c])

  # Straight
  card_type_dict = {}

  for card in cards_in_hand:
    _ , suite, _, index = card
    card_type_id = index % 13
    cards_by_type = card_type_dict.get(card_type_id, [])
    cards_by_type.append(index)
    card_type_dict[index] = cards_by_type

  card_type_keys = [k for k in card_type_dict]
  card_type_keys.sort()

  # flush

  # straight
  valid_straight_combinations = []
  for k in card_type_keys:
    sequential_keys = []
    for i in range(5):
      next_key = (k + i) % 13 
      if next_key in card_type_dict:
        sequential_keys.append(next_key)
    if len(sequential_keys) == 5:
      valid_straight_combinations.append(sequential_keys)

  def generator(arr, choices, depth, max):
    result_arr = []
    for c in choices[depth]:
      a = arr.copy()
      a.append(c)
      if depth != max:
        results = generator(a, choices, depth + 1, max)
        for r in results:
          result_arr.append(r)
      else:
        result_arr.append(a)
    return result_arr

  for comb in valid_straight_combinations:
    choices = []
    for k in comb:
      choices.append(card_type_dict[k])
    for k2 in generator([], choices, 0, 4):
      suite = k2[0] // 13
      for x in k2: # filter out straight flushes
        if x // 13 != suite:
          card_combination.append([5, k2])
          break

  # generate trios
  for t in trio:
    card_combination.append([6, t])

  # generate pairs
  for p in pair_list:
    card_combination.append([7, p])

  # generate_singles
  cards_in_hand.sort(key=sort_by_index, reverse=True)
  for p in cards_in_hand:
    _, _, _, index = p
    card_combination.append([8, [index]])
  
  return card_combination      

def compare_combinations(comb_1, comb_2):
  if comb_1 == []:
    return -1
  if comb_2 == []:
    return 1

  comb_type, cards = comb_1
  comb_type2, cards2 = comb_2
  cards.sort()
  cards2.sort()
  suite = cards[0] // 13
  suite_2 = cards2[0] // 13
  card_id = cards[0] % 13
  card_id_2 = cards2[0] % 13

  if comb_type > comb_type2:
    return -1
  elif comb_type < comb_type2:
    return 1
  
  if comb_type == 0:
    if suite > suite_2:
      return -1
    else:
      return 1

  if comb_type == 1:
    if card_id > card_id_2:
      return -1
    elif card_id < card_id_2:
      return 1

    if suite > suite_2:
      return -1
    elif suite < suite_2:
      return 1

  if comb_type in [2, 3, 6, 7, 8]:
    if card_id > card_id_2:
      return -1
    elif card_id < card_id_2:
      return 1
    if suite > suite_2:
      return -1
    elif suite < suite_2:
      return 1


  return 0
