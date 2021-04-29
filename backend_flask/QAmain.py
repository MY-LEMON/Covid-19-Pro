from QAsearch import CovidGraph
from QAsystem import EntityExtractor


class KGQA:
    def __init__(self):
        self.extractor = EntityExtractor()
        self.searcher = CovidGraph()

    def qa_main(self, input_str):
        answer = "对不起，您的问题我不知道，我今后会努力改进的。"
        entities = self.extractor.extractor(input_str)
        if not entities:
            return answer
        print(entities)
        sqls = self.searcher.question_parser(entities)
        final_answer, node_relation = self.searcher.searching(sqls)
        if not final_answer:
            return answer, []
        else:
            return final_answer, node_relation


if __name__ == "__main__":
    while True:
        handler = KGQA()
        question = input("用户：")
        if not question:
            break
        final_answer, node_relation = handler.qa_main(question)
        print("*" * 50)
