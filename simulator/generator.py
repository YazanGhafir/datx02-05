import numpy as np
import names
import pandas as pd
import datetime
from absl import flags
from absl import app
from individual import Individual
from movement import Movement

FLAGS = flags.FLAGS

flags.DEFINE_integer("n",100,"How many individuals to generate")
flags.DEFINE_integer("bpm",100,"Mean of bench press max")
flags.DEFINE_integer("bpv",5,"Variance in bench press max")
flags.DEFINE_integer("am",30,"Age mean")
flags.DEFINE_integer("av",5,"Age variance")
flags.DEFINE_float("gr", 0.5, "Gender ratio of male")

def gender_to_string(x):
    if x==0:
        return "male"
    elif x==1:
        return "female"

def generate_indviduals(num, age_mean, age_variance, bench_press_fitness_mean, bench_press_fitness_variance, gender_ratio):
    '''
    Generates individuals to be used in the simulator

    :param num: Number of individuals to generate.
    :param age_mean: The mean of the age for the individuals
    :param age_variance: The variance in age for the individuals for a normal distribution
    :param bench_press_fitness_mean: The mean of the 1RM in bench press for the individuals
    :param bench_press_fitness_variance: The variance in the 1RM for the individuals for a normal distribution
    :return: A list of individuals generated
    '''

    #Holds all individuals
    individuals = []
    
    #Normally distributed ages used to create birth dates
    ages = np.random.normal(age_mean, age_variance, num).astype("int")
    now = datetime.datetime.now()
    birth_dates = [datetime.datetime(now.year-age, now.month, now.day) for age in ages]
    
    #Normally distributed bench press fitnesses used to create bench press movementss
    bench_press_fitnesses = np.random.normal(bench_press_fitness_mean, bench_press_fitness_variance, num).astype("int")

    genders = np.ones(num)
    genders[:int(num*gender_ratio)] = 0
    np.random.shuffle(genders)  
    for i in range(num):
        name = names.get_full_name(gender=gender_to_string(genders[i]))
        bench_press_movement = Movement(1,1,bench_press_fitnesses[i],1,1,1,1)
        individual = Individual(i, birth_dates[i], int(genders[i]), name, 0, bench_press_movement)
        individuals.append(individual)

    return individuals

def save_individuals(individuals, csv_file_path):
    all_indviduals_df = pd.DataFrame(columns=['id','birth','gender','name','weight','bench_press_movement'])
    for individual in individuals:
        print(individual.to_dataframe())
        all_indviduals_df = all_indviduals_df.append(individual.to_dataframe())
    print(all_indviduals_df)
    all_indviduals_df.to_csv(csv_file_path, index=False)

def main(argv):
    generated_individuals = generate_indviduals(FLAGS.n, FLAGS.am, FLAGS.av, FLAGS.bpm, FLAGS.bpv, FLAGS.gr)
    save_individuals(generated_individuals, "individuals.csv")

if __name__ == "__main__":
    app.run(main)
