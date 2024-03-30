from heredity import *


people = {
  'Harry': {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None},
  'James': {'name': 'James', 'mother': None, 'father': None, 'trait': True},
  'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': False}
}

one_genes = {}
two_genes = {}
have_trait = {}





answer = joint_probability(people, one_genes, two_genes, have_trait)

print(answer)