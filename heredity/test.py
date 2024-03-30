from heredity import *


people = {
  'Harry': {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None},
  'James': {'name': 'James', 'mother': None, 'father': None, 'trait': True},
  'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': False}
}

one_genes = {"Harry"}
two_genes = {"James"}
have_trait = {"James"}


for person in people:
    print(person["name"])

# answer = joint_probability(people, one_genes, two_genes, have_trait)
