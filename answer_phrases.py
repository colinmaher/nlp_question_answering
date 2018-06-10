import operator
from utils import nltk, model, stopwords, pattern_matcher, match_sent_structs, get_bow, get_sentences

#function to recursively go up the dependency tree to find the word in the question we wish
#to look for in the answer
# def recursive_find_ans_word(node_indicies):
#     for dep in node['deps'].items():
#         if re.match(r'^V*', dep[0]):
#             highest_subj_ind = dep[1][0]
#         else:
#             if len(q_dep_graph.get_by_address(dep[1])['deps']) > 0:
#                 nodes_to_search += [dep[1]]
#     if highest_subj_ind == 0:
#         find_ans_word(q_dep_graph, nodes_to_search)

# def find_ans_word(q_dep_graph):
#     highest_subj_ind = 0
#     highest_subj = ''
#     root_word = ''
#     nodes_to_search = []
#     for nodeNum in q_dep_graph.nodes:
#         node = q_dep_graph.get_by_address(nodeNum)
#         # print(node)
#         if node['rel'] == 'root':
#             root_word = node['word']
#             # print('root deps:')
#             # print(node['deps'].items())
#             #if root is qword, recursively find nsub
#             # if re.match(r'^W*', node['tag']):
#             #     dep_nodes_list = []
#             #     for node in node['deps']:
#             #         dep_nodes_list.append(node[1])
#             #     recursive_find_ans_word(dep_nodes_list)
#             for dep in node['deps'].items():
#                 if q_dep_graph.get_by_address(dep[1][0])['rel'] == 'nsubj':
#                     highest_subj_ind = dep[1][0]
#     highest_subj = q_dep_graph.get_by_address(highest_subj_ind)['word']
#     if highest_subj is None:
#         for dep in node['deps'].items():
#             if q_dep_graph.get_by_address(dep[1][0])['tag'].lower()[0] == 'v':
#                 highest_subj_ind = dep[1][0]
#         if highest_subj_ind == 0:
#             highest_subj = root_word
#         else:
#             highest_subj = q_dep_graph.get_by_address(highest_subj_ind)['word']

#     # print("best q word: " + highest_subj)
#     return highest_subj

def find_answer(question, sent_dep, sent_con):
    #get right types of phrase based on question first
    qtokens = nltk.word_tokenize(question['text'])
    qword = qtokens[0].lower()
    qbow = get_bow(get_sentences(question['text'])[0], stopwords)
    
    phrases = ""
    print(sent_con)
    if qword == 'what':
        # print("sent constuency graph:")
        # for tree in sent_con.subtrees():
        #     print(tree)
        pattern = nltk.ParentedTree.fromstring("(NP)")
        phrases = pattern_matcher(pattern, sent_con)
        # pattern = nltk.ParentedTree.fromstring("(VP)")
        # phrases += pattern_matcher(pattern, sent_con)
        
    if qword == 'where':
        pattern = nltk.ParentedTree.fromstring("(PP)")
        phrases = pattern_matcher(pattern, sent_con)

    elif qword == 'who':
        pattern = nltk.ParentedTree.fromstring("(NP)")
        phrases = pattern_matcher(pattern, sent_con)
        # pattern = nltk.ParentedTree.fromstring("(NNP)")
        # phrases += pattern_matcher(pattern, sent_con)
        pattern = nltk.ParentedTree.fromstring("(MD)")
        phrases += pattern_matcher(pattern, sent_con)

    elif qword == 'when':
        pattern = nltk.ParentedTree.fromstring("(NP)")
        phrases = pattern_matcher(pattern, sent_con)
        pattern = nltk.ParentedTree.fromstring("(PP)")
        phrases += pattern_matcher(pattern, sent_con)
    
    #look at phrases with 'because'
    elif qword == 'why':
        pattern = nltk.ParentedTree.fromstring("(SBAR)")
        phrases = pattern_matcher(pattern, sent_con)

    elif qword == 'which':
        pattern = nltk.ParentedTree.fromstring("(NP)")
        phrases = pattern_matcher(pattern, sent_con)
        

    elif qword == 'how':
        # pattern = nltk.ParentedTree.fromstring("(NP)")
        # phrases = pattern_matcher(pattern, sent_con)
        pattern = nltk.ParentedTree.fromstring("(PP)")
        phrases = pattern_matcher(pattern, sent_con)
        pattern = nltk.ParentedTree.fromstring("(VP)")
        phrases += pattern_matcher(pattern, sent_con)

    
    if phrases != "":
        joined_phrases = ""
        for phrase_tree in phrases:
            phrase = phrase_tree.leaves()
            print("phrase leaves: ")
            print(phrase)
            filtered_phrases = []
            use_phrase = True
            for word in phrase:
                print("qbow: ")
                print(qbow)
                if word in qbow:
                    use_phrase = False
            if use_phrase: 
                filtered_phrases.append(" ".join(phrase))
            print("filtered phrase: ")
            print(filtered_phrases)
            if filtered_phrases != []:
                joined_phrases += " ".join(filtered_phrases) + " "
        print("phrases:")
        print(joined_phrases)
        if joined_phrases != "":
            return joined_phrases
    # best_big_verb = ''
    # best_verb = ''
    # num_deps = 0
    # num_big_deps = 0
    # noun = False

    # print (question['dep'])

    # for node in question['dep'].nodes.values():
    #     if node['tag'][0].lower() == "v":
    #         deps = get_dependents(node, question['dep'])
    #         if len(deps) > num_deps:
    #             if node['word'] not in stopwords:
    #                 num_big_deps = len(deps)
    #                 best_big_verb = node['word']
    #             else:
    #                 best_verb = node['word']
    #                 num_deps = len(deps)
    
    # print("answer dep: ")
    # print(sent_dep)

    # print("best big verb: ")
    # print(best_big_verb)
    # print(num_big_deps)
    # print()

    # print("best verb: ")
    # print(best_verb)
    # print(num_deps)


    # most_sim_verb = ''
    # sim_value = 0.0

    # for node in sent_dep.nodes.values():
    #     if node['tag'][0].lower() == 'v':
    #         if node['word'] in model.vocab and (best_verb in model.vocab or best_big_verb in model.vocab):
    #             if best_big_verb != '':
    #                 if model.similarity(node['word'], best_big_verb) > sim_value:


    # if num_deps == 0 and num_big_deps == 0:
    for node in sent_dep.nodes.values():

        if node['rel'] == "root":
            deps = get_dependents(node, sent_dep)
            
            deps = sorted(deps+[node], key=operator.itemgetter("address"))

            
            return " ".join(dep["word"] for dep in deps)


def get_dependents(node, graph):
    results = []
    for item in node["deps"]:
        address = node["deps"][item][0]
        dep = graph.nodes[address]
        results.append(dep)
        results = results + get_dependents(dep, graph)
        
    return results