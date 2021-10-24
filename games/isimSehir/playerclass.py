
class Contender:
    def __init__(self, name, categoryList):
        self.name = name
        self.score = 0
        self.categories = categoryList
        self.categoryNumbers = {category: index for index, category in enumerate(categoryList)}
        self.table = [[category] for category in categoryList]
        self.table.append(['Puan'])

    def answer(self, category, response):
        indexNumber = 1
        while True:
            try:
                getattr(self, f'{category}_{indexNumber}')
                indexNumber += 1
            except AttributeError:
                break
        setattr(self, f'{category}_{indexNumber}', response)
        self.table[self.categoryNumbers[category]].append(response)

    def change_answer(self, category, tour, newAnswer):
        setattr(self, f'{category}_{tour}', newAnswer)
        self.table[self.categoryNumbers[category]][tour] = newAnswer

    def remove_answer(self, category, tour):
        delattr(self, f'{category}_{tour}')
        del self.table[self.categoryNumbers[category]][tour]

    def score_response(self, category, tour, score):
        setattr(self, f'{category}_{tour}_score', score)

    def sum_tour(self, tour, total):
        setattr(self, f'sum_{tour}', total)
