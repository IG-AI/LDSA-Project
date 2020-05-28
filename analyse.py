import sys, time
from bson import Code
from mongodb import MongoDB


def analysis_title(collection):
    mapper = Code(
        """
        function () {
            var text = this.title
            if (text) {
                words = text.toLowerCase().split(" ")
                for(var i = words.length - 1; i >= 0; i--) {
                    word = words[i].replace(/[&\/\\#,+()$~%.'":*?<>{}]/g, '')
                    if (word != '-' && word != '') {
                        emit(word, 1);
                    }
                }
            }
        };
        """)

    reducer = Code(
        """
        function (key, values) {
            var result = 0;
            for (var i = 0; i < values.length; i++) {
                result += values[i];
            }
            return result;
        }
        """)

    return collection.map_reduce(mapper, reducer, "title_result")


def print_map_reduce(collection, amount):
    for doc in collection.find().sort("value", -1).limit(amount):
        print(doc)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        directory = sys.argv[1]
        
    MongoDB = MongoDB()

    # MongoDB.delete_collection()
    # MongoDB.add_collection(directory)

    # MongoDB.print_collection(1000)

    start_time = time.time()
    result = analysis_title(MongoDB.collection)
    elapsed_time = time.time() - start_time
    print_map_reduce(result, 10)
    print("Running time: " + elapsed_time)
