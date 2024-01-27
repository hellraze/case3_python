import io
import os
import random
import logging
import argparse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


class LatexGenerator:
    def __init__(self, head_path, q_start_path, q_start2_path, q_finish_path, tail_path, tasks_dir, students_path):
        self.random_seed = 1183
        random.seed(self.random_seed)
        self.head = self.read_file(head_path)
        self.q_start = self.read_file(q_start_path)
        self.q_start2 = self.read_file(q_start2_path)
        self.q_finish = self.read_file(q_finish_path)
        self.tail = self.read_file(tail_path)

        self.tasks = self.read_tasks(tasks_dir)
        self.students = self.read_students(students_path)

    def read_tasks(self, tasks_dir):
        result = []
        total_tasks = len(os.listdir(tasks_dir))
        logger.info(total_tasks + 1)
        for i in range(1, total_tasks):
            result.append([])
            total_variants = len(os.listdir(os.path.join(tasks_dir, str(i))))
            for k in range(1, total_variants):
                result[i - 1].append(self.read_file(os.path.join(tasks_dir, str(i), f"{k}.tex")))
        return result

    def read_students(self, students_path):
        with io.open(students_path, encoding='utf-8') as file:
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

    def make_main_tex_file(self, main_tex_path):
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

        self.make_tex_file(main_tex_path, main_content)

    def make_dump_tex_file(self, dump_tex_path):
        logger.info("Making dump.tex file...")

        dump_content = self.head
        for i in range(len(self.tasks)):
            dump_content += self.q_start + str(i + 1) + self.q_start2
            for k in range(len(self.tasks[i])):
                dump_content += self.tasks[i][k]
            dump_content += self.q_finish

        dump_content += self.tail
        self.make_tex_file(dump_tex_path, dump_content)

    def run(self, main_tex_path, dump_tex_path):
        self.make_main_tex_file(main_tex_path)
        self.make_dump_tex_file(dump_tex_path)
        logger.info("Done!")


def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate LaTeX files for students and tasks.')
    parser.add_argument('--head', required=True, help='Path to head template file')
    parser.add_argument('--q_start', required=True, help='Path to q_start template file')
    parser.add_argument('--q_start2', required=True, help='Path to q_start2 template file')
    parser.add_argument('--q_finish', required=True, help='Path to q_finish template file')
    parser.add_argument('--tail', required=True, help='Path to tail template file')
    parser.add_argument('--tasks_dir', required=True, help='Directory containing task templates')
    parser.add_argument('--students', required=True, help='Path to students file')
    parser.add_argument('--main_tex', required=True, help='Path to main.tex output file')
    parser.add_argument('--dump_tex', required=True, help='Path to dump.tex output file')

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    latex_generator = LatexGenerator(
        args.head, args.q_start, args.q_start2, args.q_finish, args.tail, args.tasks_dir, args.students
    )
    latex_generator.run(args.main_tex, args.dump_tex)
