from collections import deque

graph = {}
graph["you"] = ["tor","jerry","cry"]
graph["tor"] = ["1","2"]
graph["jerry"] = ["4","5"]
graph["cry"] = ["7","8"]
graph["1"] = []
graph["2"] = []
graph["4"] = []
graph["5"] = []
graph["7"] = ["to"]
graph["8"] = []

def person_is_seller(name):
    return name[-1] == "m"

def search(name):
    search_queue = deque()
    search_queue += graph[name]
    searched = []
    while search_queue:
        print(search_queue)
        person = search_queue.popleft()
        if person not in searched:
            if person_is_seller(person):
                print(person + " mango seller")

                return True
            else:
                search_queue += graph[person]

    return False

search("you")


