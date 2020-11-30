from random import randint


def gen_salary_data():
    with open('salary.csv', 'w') as f:
        f.write("duże miasto,rodzaj stanowiska,doświadczenie\n")
        for i in range(200):
            f.write(f"{randint(0, 1)},{randint(0, 2)},{randint(0, 2)}\n")


def gen_progress_data():
    with open('progress.csv', 'w') as f:
        f.write("stare technologie,rodzaj projektu,możliwośc zmiany teamu\n")
        for i in range(200):
            f.write(f"{randint(0, 1)},{randint(0, 2)},{randint(0, 2)}\n")


if __name__ == '__main__':
    gen_salary_data()
    gen_progress_data()
