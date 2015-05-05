import Data.List
import Data.Bits

type Item = Integer
type SetOfItems = [Item]
type SetOfSets = [SetOfItems]

numberOfSets :: SetOfSets -> Integer
-- numberOfSets 0 = 0
-- numberOfSets n = n `mod` 2 + numberOfSets (n `div` 2)
numberOfSets = fromIntegral . length

numberOfItems :: SetOfItems -> Integer
-- numberOfItems 0 = 0
-- numberOfItems n = n `mod` 2 + numberOfItems (n `div` 2)
numberOfItems = fromIntegral . length

setsIn :: Integer -> SetOfSets -> [SetOfItems]
setsIn n ss = [s | s <- [0..2^n-1], testBit ss (fromIntegral s)]

questionsNeeded :: Integer -> SetOfSets -> SetOfSets -> Integer
questionsNeeded _ possible_true_sets _
    | numberOfSets possible_true_sets == 0 = error "this is not even possible"
    | numberOfSets possible_true_sets == 1 = 0
questionsNeeded n possible_true_sets asked_questions =
    1 + minimum [questionsNeededAfterQ n possible_true_sets q | q <- [0..2^n-1], q `notElem` asked_questions]

questionsNeededAfterQ :: Integer -> SetOfSets -> SetOfItems -> Integer
questionsNeededAfterQ n possible_true_sets q = maximum [questionsNeededAfterQR n possible_true_sets q r | r<- possible_replies]
    where possible_replies = nub [numberOfItems s | s <- setsIn n possible_true_sets]

questionsNeededAfterQR :: Integer -> SetOfSets -> SetOfItems -> Integer -> Integer
questionsNeededAfterQR n possible_true_sets q r = 1
