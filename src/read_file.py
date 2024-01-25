import io
import os
import random
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


class LatexGenerator:
    def __init__(self):
        self.random_seed = 1183
        random.seed(self.random_seed)
        self.head = self.read_file('../templates/head.tex')
        self.q_start = self.read_file('../templates/qStart.tex')
        self.q_start2 = self.read_file('../templates/qStart2.tex')
        self.q_finish = self.read_file('../templates/qFinish.tex')
        self.tail = self.read_file('../templates/tail.tex')

        self.tasks = self.read_tasks()
        self.students = self.read_students()

    def read_tasks(self):
        result = []
        total_tasks = len(os.listdir('../text/tasks'))
        logger.info(total_tasks + 1)
        for i in range(1, total_tasks):
            result.append([])
            total_variants = len(os.listdir('../text/tasks/%d' % i))
            for k in range(1, total_variants):
                result[i - 1].append(self.read_file('../text/tasks/%d/%d.tex' % (i, k)))
        return result

    def read_students(self):
        with io.open("../students.txt", encoding='utf-8') as file:
            result = file.readlines()
        return result

    def generate_variants(self, total):
        counts = [len(i) for i in self.tasks]
        result = set()
        while len(result) < total:
            result.add(self.generate_variant(counts))
        return list(result)

    def generate_variant(self, counts):
        return tuple(random.randint(1, count) for count in counts)

    def read_file(self, name):
        with io.open(name, encoding='utf-8') as file:
            text = file.read()
        return text

    def make_tex_file(self, file_name, content):
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        with io.open(file_name, "w", encoding='utf-8') as out:
            out.write(content)

    def make_main_tex_file(self):
        logger.info("Making main.tex file...")
        variants = self.generate_variants(len(self.students))
        random.shuffle(variants)

        main_content = self.head
        for i in range(len(variants)):
            main_content += self.q_start + str(self.students[i]) + self.q_start2
            for task_number, task in enumerate(self.tasks):
                main_content += task[variants[i][task_number] - 1]
            main_content += self.q_finish
        main_content += self.tail

        self.make_tex_file("../text/latex/main.tex", main_content)

    def make_dump_tex_file(self):
        logger.info("Making dump.tex file...")

        dump_content = self.head
        for i in range(len(self.tasks)):
            dump_content += self.q_start + str(i + 1) + self.q_start2
            for k in range(len(self.tasks[i])):
                dump_content += self.tasks[i][k]
            dump_content += self.q_finish

        dump_content += self.tail
        self.make_tex_file("../text/latex/dump.tex", dump_content)

    def run(self):
        self.make_main_tex_file()
        self.make_dump_tex_file()
        logger.info("Done!")


if __name__ == "__main__":
    latex_generator = LatexGenerator()
    latex_generator.run()
