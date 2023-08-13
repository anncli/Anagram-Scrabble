from itertools import combinations
import copy

class AnagramExplorer:
    def __init__(self, all_words: list[str]):
       self.__corpus = all_words
       self.anagram_lookup = self.get_lookup_dict() # Only calculated once, when the object is created

    @property
    def corpus(self):
      return self.__corpus

    def is_valid_anagram_pair(self, pair:tuple[str], letters:list[str]) -> bool:
        '''Checks whether a pair of words:
            -are both included in the allowable word list (self.corpus)
            -consist entirely of letters chosen at the beginning of the game
            -form a valid anagram pair

            Args:
                pair: A tuple of two strings
                letters: The letters from which the anagrams should be created

            Returns:
                bool: Returns True if the word pair fulfills all validation requirements, otherwise returns False
        '''
        if pair[0].lower() not in self.corpus or pair[1].lower() not in self.corpus or pair[0].lower() == pair[1].lower():
          return False

        for word in pair:
            word = str(word).lower()
            letters_copy = copy.copy(letters)
            for letter in word:
                if letter in letters_copy:
                    letters_copy.remove(letter)
                elif letter not in letters_copy:
                    return False

        return sorted(str(pair[0]).lower()) == sorted(str(pair[1]).lower())
    
    
    def get_lookup_dict(self) -> dict:
        '''Creates a fast dictionary look-up (via prime hash or sorted tuple) of all anagrams in a word corpus.
       
        Args:
            corpus (list): A list of words which should be considered

        Returns:
            dict: Returns a dictionary with keys that return sorted lists of all anagrams of the key (per the corpus)
        '''
        lookup_dict = {}
        sorted_corpus = sorted(self.corpus)

        for h in sorted_corpus:
            if tuple(sorted(h)) in lookup_dict:
                lookup_dict[tuple(sorted(h))].append(h)
            else:
                lookup_dict[tuple(sorted(h))] = [h]

        return lookup_dict
    

    def get_all_anagrams(self, letters: list[str]) -> set:
        '''Creates a set of all unique words that could have been used to form an anagram pair.
           Words which can't create any anagram pairs should not be included in the set.

           Ex)
            corpus: ["abed", "mouse", "bead", "baled", "abled", "rat", "blade"]
            all_anagrams: {"abed",  "abled", "baled", "bead", "blade"}

           Args:
              letters (list): A list of letters from which the anagrams should be created

           Returns:
              set: all unique words in corpus which form at least 1 anagram pair
        '''
        all_anagrams = set()
        lookup_dict = self.anagram_lookup
        for key in lookup_dict:
            inLetters = True
            letters1 = copy.copy(letters)
            for i in range(len(key)): #check if lookup_dict key is in letters
                if key[i] in letters1:
                    letters1.remove(key[i])
                elif key[i] not in letters1:
                    inLetters = False
            if len(lookup_dict[key]) > 1 and inLetters == True: #has valid anagram
               for i in range(len(lookup_dict[key])):
                  if len(lookup_dict[key][i]) > 2: #valid word must be >2 letters long
                    all_anagrams.add(lookup_dict[key][i])
        return all_anagrams


    def get_most_anagrams(self, letters:list[str]) -> list[str]:
        '''Returns a word from the largest list of anagrams that can be formed using the given letters.'''
        lookup_dict = self.anagram_lookup
        max_anagrams = 1
        key_max = None
        for key in lookup_dict:
            inLetters = True
            letters_copy = copy.copy(letters)
            for i in range(len(key)): #check if lookup_dict key is in letters
                if key[i] in letters_copy:
                    letters_copy.remove(key[i])
                else:
                    inLetters = False
                    break
            # update max length
            if len(lookup_dict[key]) > max_anagrams and inLetters == True:
                max_anagrams = len(lookup_dict[key])
                key_max = key

        return lookup_dict[key_max][0]
    

if __name__ == "__main__":
  print("Running AnagramExplorer for testing")
  words1 = [
     "abed","abet","abets","abut","acme","acre","acres","actors","actress","airmen","alert","alerted","ales","aligned","allergy","alter","altered","amen","anew","angel","angle","antler","apt",
     "bade","baste","bead","beast","beat","beats","beta","betas","came","care","cares","casters","castor","costar","dealing","deer", "gallery","glean","largely","later","leading","learnt","leas","mace","mane",
     "marine","mean","name","pat","race","races","recasts","reed", "regally","related","remain","rental","sale","scare","seal","tabu","tap","treadle","tuba","wane","wean"
  ]

  words2 = ["rat", "mouse", "tar", "art", "chicken", "stop", "pots", "tops", "reed", "deer", "fart", "tarf"]

  letters = ["r", "e", "d", "a"]

  my_explorer = AnagramExplorer(words2)

  print(my_explorer.is_valid_anagram_pair(("reed", "deer"), letters))
  print(my_explorer.is_valid_anagram_pair(("stop", "pots"), letters))
  #print(my_explorer.get_most_anagrams(letters))
  print(my_explorer.get_all_anagrams(letters))