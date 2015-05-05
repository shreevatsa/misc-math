import Data.List
import Data.Bits

type Item = Integer
type SetOfItems = Integer
type SetOfSets = Integer

numberOfSets :: SetOfSets -> Integer
numberOfSets 0 = 0
numberOfSets n = n `mod` 2 + numberOfSets (n `div` 2)

numberOfItems :: SetOfItems -> Integer
numberOfItems 0 = 0
numberOfItems n = n `mod` 2 + numberOfItems (n `div` 2)

setIn :: Integer -> SetOfSets -> SetOfItems -> Bool
setIn n ss q = testBit ss (fromIntegral q) -- Warning sign

setsIn :: Integer -> SetOfSets -> [SetOfItems]
setsIn n ss = [s | s <- [0..2^n-1], setIn n ss s]

setFrom :: [SetOfItems] -> SetOfSets
setFrom xs | xs /= nub xs = error "Set has duplicates"
setFrom [] = 0
setFrom (x:xs) = (2^x) .|. (setFrom xs)

a :: Integer -> Integer
a n = questionsNeeded n (2^(2^n)-1) 0

addToSet :: SetOfSets -> SetOfItems -> SetOfSets
addToSet asked q = asked `setBit` (fromIntegral q)

questionsNeeded :: Integer -> SetOfSets -> SetOfSets -> Integer
questionsNeeded _ possible_true_sets _
    | numberOfSets possible_true_sets == 0 = error "this is not even possible"
    | numberOfSets possible_true_sets == 1 = 0
questionsNeeded n possible_true_sets asked_questions =
    1 + minimum [questionsNeededAfterQ n possible_true_sets q asked_questions | q <- [1..2^n-1], not $ setIn n asked_questions q]

questionsNeededAfterQ :: Integer -> SetOfSets -> SetOfItems -> SetOfSets -> Integer
questionsNeededAfterQ n _ q _ | q > 2^n-1 = error "Cannot ask q as a question"
questionsNeededAfterQ n possible_true_sets q asked
    = maximum [questionsNeededAfterQR n possible_true_sets q r asked | r<- possible_replies]
    where possible_replies = nub [numberOfItems (s .&. q) | s <- setsIn n possible_true_sets] -- This is not right: global, not q-specific

questionsNeededAfterQR :: Integer -> SetOfSets -> SetOfItems -> Integer -> SetOfSets -> Integer
questionsNeededAfterQR n possible_true_sets q r asked = questionsNeeded n still_possible_true_sets (addToSet asked q)
    where
      still_possible_true_sets :: SetOfSets
      still_possible_true_sets = setFrom [s | s <- setsIn n possible_true_sets, numberOfItems (s .&. q) == r]
